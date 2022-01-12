from math import prod


class BITS:
    def __init__(self, list_of_binary: list[str]):
        self.digits = []
        for num in list_of_binary:
            if num.startswith("0b"):
                binnum = num[2:]
            else:
                binnum = num
            if (digit_no := len(binnum)) < 4:
                self.digits.extend(["0"] * (4 - digit_no))
            self.digits.extend([x for x in binnum])

    @classmethod
    def from_hex(cls, hex_str: str):
        binary_strings = [bin(int(x, 16)) for x in hex_str]
        return cls(binary_strings)

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            content = f.read().strip()
        return cls.from_hex(content)

    def parse_packets(self):
        return Packet(self.digits)


class Packet:
    def __init__(self, binary: list[str]):
        self.version = int("".join(binary[:3]), 2)
        self.packet_type = int("".join(binary[3:6]), 2)
        self.binary = binary
        self.subpackets = []
        if self.packet_type == 4:
            self.literal_value = self.parse_literal()
        else:
            self.literal_value = None
            self.length_type = self.binary[6]
            if self.length_type == "0":
                self.parse_bitlength_operator()
            else:
                self.parse_subnum_operator()
        self.packet_length = len(self.binary)

    def __repr__(self):
        return f"Packet({self.version},{self.packet_type},{self.literal_value},{len(self.subpackets)},{self.packet_length})"

    def output_tuple(self):
        if self.subpackets:
            return (self, [s.output_tuple() for s in self.subpackets])
        else:
            return (self, None)

    def version_sum(self):
        final_sum = self.version
        if self.subpackets:
            for s in self.subpackets:
                final_sum += s.version_sum()
        return final_sum

    def parse_literal(self):
        output = []
        last_group = False
        for i, n in enumerate(self.binary[6:]):
            if (step := i % 5) == 0:
                if n == "0":
                    last_group = True
                continue
            else:
                output.append(n)
            if step == 4:
                if last_group:
                    self.binary = self.binary[: i + 7]
                    return int("".join(output), 2)

    def parse_bitlength_operator(self):
        total_subpacket_length = int("".join(self.binary[7:22]), 2)
        starting_idx = 22
        while starting_idx < (my_length := total_subpacket_length + 22):
            next_packet = Packet(self.binary[starting_idx:])
            self.subpackets.append(next_packet)
            starting_idx += next_packet.packet_length
        self.binary = self.binary[:my_length]

    def parse_subnum_operator(self):
        total_n_subpackets = int("".join(self.binary[7:18]), 2)
        starting_idx = 18
        while len(self.subpackets) < total_n_subpackets:
            next_packet = Packet(self.binary[starting_idx:])
            self.subpackets.append(next_packet)
            starting_idx += next_packet.packet_length
        self.binary = self.binary[:starting_idx]

    def evaluate(self):
        if self.packet_type == 4:
            return self.literal_value
        else:
            subpacket_results = [s.evaluate() for s in self.subpackets]
            if self.packet_type == 0:
                return sum(subpacket_results)
            elif self.packet_type == 1:
                return prod(subpacket_results)
            elif self.packet_type == 2:
                return min(subpacket_results)
            elif self.packet_type == 3:
                return max(subpacket_results)
            elif self.packet_type == 5:
                return int(subpacket_results[0] > subpacket_results[1])
            elif self.packet_type == 6:
                return int(subpacket_results[0] < subpacket_results[1])
            elif self.packet_type == 7:
                return int(subpacket_results[0] == subpacket_results[1])


transmission = BITS.from_file("input.txt")
packet = transmission.parse_packets()
# part one
print(packet.version_sum())
# part two
print(packet.evaluate())
