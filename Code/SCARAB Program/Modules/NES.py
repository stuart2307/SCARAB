import os
from time import sleep
import serial
import zlib

from Modules import Module_Base


class nes_module(Module_Base.scarab_module):
    """
    NES/Famicom cartridge module.

    Identification strategy (mirrors OSCR nes.txt approach):
      1. Read 8KB from $8000 (no bank switching) -> CRC32 -> look up in nes.txt
         second field (bank_crc).
      2. If no match, try 8KB from $E000 (for MMC3 whose $8000 may be garbage).
      3. If still no match, fall back to progressive PRG reads (16KB -> 32KB ->
         64KB ... up to 512KB), re-hashing cumulative data, narrowing candidates
         each round until one remains or we run out of data to read.
      4. On a unique match the iNES header from the database is parsed for all
         cart parameters. On an ambiguous match the smallest-PRG candidate is
         chosen and flagged.

    nes.txt line format (OSCR):
        Game Name.nes FULL_CRC32,BANK_CRC32,<32-hex-char iNES header>

    iNES header byte positions (16 bytes):
        0-3   Magic 'NES\x1a'
        4     PRG-ROM size (x 16 KB)
        5     CHR-ROM size (x 8 KB, 0 = CHR-RAM)
        6     Flags 6 (lower mapper nibble, mirroring, battery, trainer)
        7     Flags 7 (upper mapper nibble, NES 2.0 indicator)
        8     PRG-RAM size (iNES 1) / mapper MSB (NES 2.0)
        9     TV system / CHR-RAM size (NES 2.0)
        10-15 Unused / NES 2.0 extended fields
    """

    # ------------------------------------------------------------------ #
    #  Firmware op-codes (must match Arduino sketch)                      #
    # ------------------------------------------------------------------ #
    OP_TEST_PRG_PINS = 0x21
    OP_TEST_CHR_PINS = 0x22
    OP_CRC_PRG = 0x31
    OP_CRC_CHR = 0x32
    OP_DUMP_SAVE = 0x50
    OP_RESTORE_SAVE = 0x51
    OP_DUMP_PRG = 0x70
    OP_DUMP_CHR = 0x71
    # New op: read N x 8 KB of PRG from a fixed base address, no switching.
    # Args: [op, base_page (0=$8000 / 1=$E000), num_8kb_banks]
    OP_READ_PRG_BANKS = 0x60

    # Progressive read steps in 16 KB PRG-bank units
    _PRG_STEPS = [1, 2, 4, 8, 16, 32]  # 16, 32, 64, 128, 256, 512 KB

    # ------------------------------------------------------------------ #
    #  Module interface                                                   #
    # ------------------------------------------------------------------ #

    def getIdString(self):
        return "NES"

    #     # ------------------------------------------------------------------ #
    #  nes.txt database                                                   #
    # ------------------------------------------------------------------ #
    def _db_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "nes.txt")
 
    def _load_db(self) -> list:
        """
        Parse nes.txt into a list of dicts with keys:
          name, full_crc, bank_crc, header_hex, header_bytes
        """
        entries = []
        db = self._db_path()
        if not os.path.exists(db):
            print(f"[NES] WARNING: database not found at {db}")
            return entries
 
        with open(db, encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]
 
        # Format: name line followed by data line
        #   Game Name.nes
        #   FULL_CRC,BANK_CRC,HEADERHEX
        i = 0
        while i < len(lines) - 1:
            name_line = lines[i]
            data_line = lines[i + 1]
            # Data line must have exactly 2 commas and no spaces
            if name_line.endswith(".nes") and "," in data_line and " " not in data_line:
                try:
                    fields = data_line.split(",")
                    if len(fields) == 3:
                        full_crc, bank_crc, header_hex = fields
                        header_bytes = bytes.fromhex(header_hex)
                        if len(header_bytes) == 16:
                            entries.append({
                                "name":         name_line,
                                "full_crc":     full_crc.upper(),
                                "bank_crc":     bank_crc.upper(),
                                "header_hex":   header_hex.upper(),
                                "header_bytes": header_bytes,
                            })
                            i += 2
                            continue
                except Exception:
                    pass
            i += 1
 
        print(f"[NES] Loaded {len(entries)} entries from database.")
        return entries
 
    def _parse_header(self, header: bytes) -> dict:
        """
        Decode a 16-byte iNES header into cartridge parameters.
        Handles both iNES 1.0 and NES 2.0.
        """
        if header[0:4] != b'NES\x1a':
            raise ValueError("Not a valid iNES header")
 
        nes20 = (header[7] & 0x0C) == 0x08
 
        prg_banks = header[4]  # x 16 KB
        chr_banks = header[5]  # x 8 KB (0 = CHR-RAM)
 
        flags6 = header[6]
        flags7 = header[7]
 
        mapper = ((flags6 >> 4) & 0x0F) | (flags7 & 0xF0)
        if nes20:
            mapper |= (header[8] & 0x0F) << 8
 
        has_battery = bool(flags6 & 0x02)
        has_trainer = bool(flags6 & 0x04)
        mirroring   = "vertical" if (flags6 & 0x01) else "horizontal"
        four_screen = bool(flags6 & 0x08)
 
        return {
            "mapper":      mapper,
            "prg_banks":   prg_banks,
            "chr_banks":   chr_banks,
            "prg_size_kb": prg_banks * 16,
            "chr_size_kb": chr_banks * 8,
            "has_chr_rom": chr_banks > 0,
            "has_battery": has_battery,
            "has_trainer": has_trainer,
            "mirroring":   mirroring,
            "four_screen": four_screen,
            "nes20":       nes20,
            "savesize":    0x2000 if has_battery else 0,
        }
 
    # ------------------------------------------------------------------ #
    #  Cartridge detection                                                #
    # ------------------------------------------------------------------ #
    def _read_prg_banks(self, device: serial.Serial, from_e000: bool, num_8kb: int) -> bytes:
        page = 1 if from_e000 else 0
        expected = num_8kb * 0x2000
        device.write(bytes([self.OP_READ_PRG_BANKS, page, num_8kb]))
        data = b''
        for _ in range(expected // 64):
            chunk = device.read(64)
            if len(chunk) < 64:
                break
            data += chunk
            device.write(b'K')
        return data
 
    def detectCartridge(self, device: serial.Serial, cartDetails: dict) -> bool:
        raw = self._read_prg_banks(device, False, 1)
        if len(raw) < 0x2000:
            return False
        if len(set(raw)) == 1:
            print(raw)
            print("womp womp")
            return False
        print(raw)

        db = self._load_db()
        if db:
            for from_e000 in (False, True):
                raw = self._read_prg_banks(device, from_e000, 1)
                bank_crc = f"{zlib.crc32(raw) & 0xFFFFFFFF:08X}"
                candidates = [e for e in db if e["bank_crc"] == bank_crc]
                if len(candidates) > 0:
                    result = self._progressive_match(device, candidates, cartDetails)
                    if result:
                        return True

            self._progressive_match(device, db, cartDetails)

        return True
 
    def _progressive_match(self, device: serial.Serial, candidates: list, cartDetails: dict) -> bool:
        accumulated = b''

        for prg_banks_16k in self._PRG_STEPS:
            target_bytes  = prg_banks_16k * 0x4000
            to_read_bytes = target_bytes - len(accumulated)
            if to_read_bytes <= 0:
                continue

            chunks_8kb = to_read_bytes // 0x2000
            chunk = self._read_prg_banks(device, False, chunks_8kb)
            if len(chunk) < to_read_bytes:
                break

            accumulated = accumulated + chunk
            running_crc = f"{zlib.crc32(accumulated) & 0xFFFFFFFF:08X}"

            still_possible = []
            for c in candidates:
                parsed      = self._parse_header(c["header_bytes"])
                c_prg_bytes = parsed["prg_banks"] * 0x4000

                if c_prg_bytes <= len(accumulated):
                    # We have at least as much data as this game's full PRG.
                    # Trim accumulated to its exact size and check the CRC.
                    trimmed = accumulated[:c_prg_bytes]
                    trimmed_crc = f"{zlib.crc32(trimmed) & 0xFFFFFFFF:08X}"
                    if trimmed_crc == c["full_crc"]:
                        still_possible.append(c)
                else:
                    # Haven't read enough of this game yet, keep it
                    still_possible.append(c)

            candidates = still_possible

            if len(candidates) == 0:
                return False
            if len(candidates) == 1:
                return self._apply_match(candidates[0], cartDetails)

        if candidates:
            return self._pick_best(candidates, cartDetails, ambiguous=True)
        return False
 
    def _pick_best(self, candidates: list, cartDetails: dict, ambiguous: bool = False) -> bool:
        """Choose the candidate with the smallest PRG when still ambiguous."""
        candidates_sorted = sorted(
            candidates,
            key=lambda c: self._parse_header(c["header_bytes"])["prg_banks"]
        )
        best = candidates_sorted[0]
        return self._apply_match(best, cartDetails, ambiguous=ambiguous)
 
    def _apply_match(self, entry: dict, cartDetails: dict, ambiguous: bool = False) -> bool:
        """Populate cartDetails from a matched nes.txt entry."""
        parsed = self._parse_header(entry["header_bytes"])
        cartDetails.update(parsed)
        cartDetails["name"] = entry["name"].removesuffix(".nes")
        cartDetails["checksum"] = entry["full_crc"]
        cartDetails["bank_crc"] = entry["bank_crc"]
        cartDetails["header_hex"] = entry["header_hex"]
        cartDetails["header_bytes"] = entry["header_bytes"]
        cartDetails["saveexp"] = int(cartDetails["savesize"]) // 1024
 
        if parsed["has_chr_rom"]:
            cartDetails["romsize"] = f"{parsed['prg_size_kb']}KB PRG + {parsed['chr_size_kb']}KB CHR"
        else:
            cartDetails["romsize"] = f"{parsed['prg_size_kb']}KB PRG + CHR-RAM"
        if ambiguous:
            print("Identification may be inaccurate")
        return True
 
    # ------------------------------------------------------------------ #
    #  Pin testing                                                        #
    # ------------------------------------------------------------------ #
    def testPins(self, device: serial.Serial, cartDetails: dict) -> bool:
        mapper    = cartDetails["mapper"]
        prg_banks = cartDetails["prg_banks"]
        chr_banks = cartDetails.get("chr_banks", 0)
        has_chr   = cartDetails.get("has_chr_rom", True)
        ok = True
 
        print("Testing PRG data pins...")
        device.write(bytes([self.OP_TEST_PRG_PINS, mapper, prg_banks]))
        result = device.read(2)
        device.reset_input_buffer()
        if len(result) < 2:
            print("No response for PRG pin test.")
            return False
        if result[0] != 0xFF:
            print(f"PRG pins never pulled low:  {bin(result[0] ^ 0xFF)}")
            ok = False
        if result[1] != 0xFF:
            print(f"PRG pins never pulled high: {bin(result[1] ^ 0xFF)}")
            ok = False
        if ok:
            print("All PRG pins toggled correctly.")
 
        if has_chr and chr_banks > 0:
            print("Testing CHR data pins...")
            device.write(bytes([self.OP_TEST_CHR_PINS, mapper, chr_banks]))
            result = device.read(2)
            device.reset_input_buffer()
            if len(result) < 2:
                print("No response for CHR pin test.")
                return False
            chr_ok = True
            if result[0] != 0xFF:
                print(f"CHR pins never pulled low:  {bin(result[0] ^ 0xFF)}")
                chr_ok = False
            if result[1] != 0xFF:
                print(f"CHR pins never pulled high: {bin(result[1] ^ 0xFF)}")
                chr_ok = False
            if chr_ok:
                print("All CHR pins toggled correctly.")
            ok = ok and chr_ok
 
        return ok
 
    # ------------------------------------------------------------------ #
    #  Checksum                                                           #
    # ------------------------------------------------------------------ #
    def calculateChecksum(self, device: serial.Serial, cartDetails: dict) -> bool:
        rom = self.dumpRom(device, cartDetails)
        # Strip the 16 byte iNES header before hashing, matching nes.txt
        computed = f"{zlib.crc32(rom[16:]) & 0xFFFFFFFF:08X}"
        expected = cartDetails.get("checksum", "")
        match    = computed.upper() == expected.upper()
        return match
    #    mapper    = cartDetails["mapper"]
    #    prg_banks = cartDetails["prg_banks"]
    #    chr_banks = cartDetails.get("chr_banks", 0)
    #    has_chr   = cartDetails.get("has_chr_rom", True)
 #
    #    device.write(bytes([self.OP_CRC_PRG, mapper, prg_banks]))
    #    prg_crc = int.from_bytes(device.read(4), "big")
    #    print(f"PRG CRC32: 0x{prg_crc:08X}")
 #
    #    if has_chr and chr_banks > 0:
    #        device.write(bytes([self.OP_CRC_CHR, mapper, chr_banks]))
    #        chr_crc = int.from_bytes(device.read(4), "big")
    #        print(f"CHR CRC32: 0x{chr_crc:08X}")
 #
    #    # nes.txt full_crc is over the PRG data only (no header)
    #    computed = f"{prg_crc:08X}"
    #    expected = cartDetails.get("checksum", "")
    #    match    = computed.upper() == expected.upper()
    #    print(f"CRC match: {'YES' if match else 'NO'} "
    #          f"(got {computed}, expected {expected})")
    #    return match
 
    # ------------------------------------------------------------------ #
    #  Save retention test (stub)                                         #
    # ------------------------------------------------------------------ #
    def testSaveRetention(self, device: serial.Serial, cartDetails: dict) -> bool:
        return True
 
    # ------------------------------------------------------------------ #
    #  ROM dump                                                           #
    # ------------------------------------------------------------------ #
    def dumpRom(self, device: serial.Serial, cartDetails: dict) -> bytes:
        """Dump PRG + CHR and return a complete iNES-headered ROM image."""
        mapper    = cartDetails["mapper"]
        prg_banks = cartDetails["prg_banks"]
        chr_banks = cartDetails.get("chr_banks", 0)
        has_chr   = cartDetails.get("has_chr_rom", True)
 
        prg_size = prg_banks * 0x4000
        chr_size = (chr_banks * 0x2000) if (has_chr and chr_banks > 0) else 0
 
        print(f"Dumping PRG ROM ({prg_size // 1024} KB)...")
        device.write(bytes([self.OP_DUMP_PRG, mapper, prg_banks]))
        prg_data = device.read(prg_size)
        print(f"  Received {len(prg_data)} / {prg_size} bytes.")
 
        chr_data = b''
        if chr_size > 0:
            print(f"Dumping CHR ROM ({chr_size // 1024} KB)...")
            device.write(bytes([self.OP_DUMP_CHR, mapper, chr_banks]))
            chr_data = device.read(chr_size)
            print(f"  Received {len(chr_data)} / {chr_size} bytes.")
 
        # Prefer the exact header from the database
        header = cartDetails.get("header_bytes") or \
                 self._build_ines_header(mapper, prg_banks, chr_banks if has_chr else 0)
        return header + prg_data + chr_data
 
    def _build_ines_header(self, mapper: int, prg_banks: int,
                           chr_banks: int) -> bytes:
        """Fallback: construct a minimal iNES 1.0 header."""
        h = bytearray(16)
        h[0:4] = b'NES\x1a'
        h[4] = prg_banks
        h[5] = chr_banks
        h[6] = (mapper & 0x0F) << 4
        h[7] = mapper & 0xF0
        return bytes(h)
 
    # ------------------------------------------------------------------ #
    #  Save dump / restore                                                #
    # ------------------------------------------------------------------ #
    def dumpSave(self, device: serial.Serial, cartDetails: dict) -> bytes:
        print("Dumping NES SRAM (8 KB)...")
        device.write(bytes([self.OP_DUMP_SAVE]))
        data = device.read(0x2000)
        print(f"  Received {len(data)} bytes.")
        return data
 
    def restoreSave(self, device: serial.Serial, cartDetails: dict,buffer: bytes) -> bool:
        print("Restoring NES SRAM...")
        device.write(bytes([self.OP_RESTORE_SAVE]))
        chunk_size = 64
        for i in range(0, len(buffer), chunk_size):
            while device.in_waiting < 1:
                continue
            if device.read(1) != b'M':
                print(f"Unexpected handshake at offset {i}.")
                return False
            chunk = buffer[i:i + chunk_size]
            if len(chunk) < chunk_size:
                chunk = chunk.ljust(chunk_size, b'\xff')
            device.write(chunk)
            while device.in_waiting < 1:
                continue
            if device.read(1) != b'K':
                print(f"Bad acknowledgement at offset {i}.")
                return False
        print("SRAM restore complete.")
        return True
 