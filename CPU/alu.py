class ALU:
    from CPU.flags import Flags
    def __init__(self):
        
        self.MASK = (1 << 52) - 1        # 0xFFFFFFFFFFFFF
        self.SIGN_BIT = 1 << 51          # 0x8000000000000

    def _update_common_flags(self, result):
        """Updates ZF and NF which are calculated the same way for most ops."""
        self.Flags.ZF = 1 if (result & self.MASK) == 0 else 0
        self.Flags.NF = 1 if (result & self.SIGN_BIT) else 0

    def add(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        
        raw_sum = val_a + val_b
        result = raw_sum & self.MASK
        
        # Flags
        self.Flags.CF = 1 if raw_sum > self.MASK else 0
        self._update_common_flags(result)
        
        # Overflow: (pos+pos=neg) or (neg+neg=pos)
        a_sig = val_a & self.SIGN_BIT
        b_sig = val_b & self.SIGN_BIT
        res_sig = result & self.SIGN_BIT
        self.Flags.OF = 1 if (a_sig == b_sig and res_sig != a_sig) else 0
        
        return format(result, '013X')

    def subtract(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        
        raw_diff = val_a - val_b
        result = raw_diff & self.MASK
        
        # Flags
        self.Flags.CF = 1 if val_a < val_b else 0 # Borrow
        self._update_common_flags(result)
        
        # Overflow: (pos-neg=neg) or (neg-pos=pos)
        a_sig = val_a & self.SIGN_BIT
        b_sig = val_b & self.SIGN_BIT
        res_sig = result & self.SIGN_BIT
        self.Flags.OF = 1 if (a_sig != b_sig and res_sig == b_sig) else 0
        
        return format(result, '013X')

    def multiply(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        
        raw_prod = val_a * val_b
        result = raw_prod & self.MASK
        
        # Carry Flag in multiplication often indicates the result 
        # exceeded the register size (upper bits were lost)
        self.Flags.CF = 1 if raw_prod > self.MASK else 0
        
        # Overflow Flag for signed multiplication is complex; 
        # here we check if the truncated result matches the expected sign
        self._update_common_flags(result)
        
        return format(result, '013X')

    def divide(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        
        if val_b == 0:
            # Handle Division by Zero based on your architecture's spec
            # Usually, this sets an error flag or keeps flags unchanged
            self.Flags.IF = 1
            return "0000000000000"

            
        # Integer division
        result = val_a // val_b
        
        # In division, CF is usually cleared (0) as there is no "carry"
        self.Flags.CF = 0
        self._update_common_flags(result)
        
        return format(result, '013X')
    
    def modulo(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        
        if val_b == 0:
            self.Flags.IF = 1
            return "0000000000000"
        
        result = val_a % val_b
        
        # Modulo doesn't typically affect CF, but we can set it to 0
        self.Flags.CF = 0
        self._update_common_flags(result)
        
        return format(result, '013X')
    
    def increment(self, a_str):
        return self.add(a_str, "1")
    
    def decrement(self, a_str):
        return self.subtract(a_str, "1")
    

    def bitwise_and(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        result = val_a & val_b
        
        # Logical ops usually clear CF and OF
        self.Flags.CF = 0
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')

    def bitwise_or(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        result = val_a | val_b
        
        self.Flags.CF = 0
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')

    def bitwise_xor(self, a_str, b_str):
        val_a = int(a_str, 16)
        val_b = int(b_str, 16)
        result = val_a ^ val_b
        
        self.Flags.CF = 0
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')

    def bitwise_not(self, a_str):
        val_a = int(a_str, 16)
        # Flip all bits and mask to exactly 52 bits
        result = (~val_a) & self.MASK
        
        self.Flags.CF = 0
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')
    
    def bitwise_nand(self, a_str, b_str):
        return self.bitwise_not(self.bitwise_and(a_str, b_str))
    
    def bitwise_nor(self, a_str, b_str):
        return self.bitwise_not(self.bitwise_or(a_str, b_str))
    
    def shl(self, a_str, n_str):
        val_a = int(a_str, 16)
        n = int(n_str, 16)
        
        if n <= 0: return format(val_a, '013X')
        if n > 52: n = 52 # Cap shift at word size
        
        # The Carry Flag is usually the LAST bit shifted out
        # It is the bit at index (52 - n)
        if n <= 52:
            self.Flags.CF = (val_a >> (52 - n)) & 1
        else:
            self.Flags.CF = 0
            
        result = (val_a << n) & self.MASK
        
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')

    def shr(self, a_str, n_str):
        val_a = int(a_str, 16)
        n = int(n_str, 16)
        
        if n <= 0: return format(val_a, '013X')
        
        # The Carry Flag is the last bit shifted out from the right
        # It is the bit at index (n - 1)
        if n <= 52:
            self.Flags.CF = (val_a >> (n - 1)) & 1
        else:
            self.Flags.CF = 0

        result = (val_a >> n) & self.MASK
        
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')
    
    def rol(self, a_str, n_str):
        val_a = int(a_str, 16)
        n = int(n_str, 16) % 52 # 52nd rotation returns to start
        
        if n == 0: return format(val_a, '013X')
        
        # Logic: Shift left by N, then OR with the bits that "fell off" the left
        # and are now appearing on the right.
        result = ((val_a << n) & self.MASK) | (val_a >> (52 - n))
        
        # CF is the last bit wrapped around
        self.Flags.CF = (result & 1) 
        
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')

    def ror(self, a_str, n_str):
        val_a = int(a_str, 16)
        n = int(n_str, 16) % 52
        
        if n == 0: return format(val_a, '013X')
        
        # Logic: Shift right by N, then OR with the bits that "fell off" the right
        # and are now appearing on the left.
        result = (val_a >> n) | ((val_a << (52 - n)) & self.MASK)
        
        # CF is the last bit wrapped around
        self.Flags.CF = (result >> 51) & 1
        
        self.Flags.OF = 0
        self._update_common_flags(result)
        return format(result, '013X')
    

alu = ALU()
