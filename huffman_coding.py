import os
import heapq

class BinaryTreeNode:
    def __init__(self, value, freq):
        # Initialize a binary tree node with value and frequency
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        # Compare nodes based on frequency for heap operations
        return self.freq < other.freq
    
    def __eq__(self, other):
        # Check if two nodes have the same frequency
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self, path):
        # Initialize HuffmanCoding with the file path
        self.path = path
        self.__heap = []
        self.__codes = {}
        self.__reverseCodes = {}
        
    def __make_frequency_dict(self, text):
        # Create a frequency dictionary from the text
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0
            freq_dict[char] += 1
        return freq_dict

    def __buildHeap(self, freq_dict):
        # Build a heap of binary tree nodes based on frequency dictionary
        for key in freq_dict:
            frequency = freq_dict[key]
            binary_tree_node = BinaryTreeNode(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __buildTree(self):
        # Build the Huffman tree by combining nodes with the lowest frequency
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap)
            binary_tree_node_2 = heapq.heappop(self.__heap)
            freq_sum = binary_tree_node_1.freq + binary_tree_node_2.freq
            newNode = BinaryTreeNode(None, freq_sum)
            newNode.left = binary_tree_node_1
            newNode.right = binary_tree_node_2
            heapq.heappush(self.__heap, newNode)

    def __buildCodesHelper(self, root, curr_bits):
        # Helper function to build Huffman codes by traversing the tree
        if root is None:
            return 
        if root.value is not None:
            self.__codes[root.value] = curr_bits
            self.__reverseCodes[curr_bits] = root.value
            return
        self.__buildCodesHelper(root.left, curr_bits + "0")
        self.__buildCodesHelper(root.right, curr_bits + "1")

    def __buildCodes(self):
        # Build Huffman codes from the tree
        root = heapq.heappop(self.__heap)
        self.__buildCodesHelper(root, "")

    def __getEncodedText(self, text):
        # Encode the text using the Huffman codes
        encoded_text = ""
        for char in text:
            encoded_text += self.__codes[char]
        return encoded_text

    def __getPaddedEncodedText(self, encoded_text):
        # Pad the encoded text to make its length a multiple of 8
        padded_amount = 8 - (len(encoded_text) % 8)
        for i in range(padded_amount):
            encoded_text += '0'
        padded_info = "{0:08b}".format(padded_amount)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def __getBytesArray(self, padded_encoded_text):
        # Convert the padded encoded text to a byte array
        array = []
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            array.append(int(byte, 2))
        return array
        
    def compress(self):
        # Compress the file at the given path
        file_name, file_extension = os.path.splitext(self.path)
        output_path = file_name + ".bin"
        
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            # Read the file text and remove trailing whitespace
            text = file.read().rstrip()
            # Create a frequency dictionary
            freq_dict = self.__make_frequency_dict(text)
            # Build a heap from the frequency dictionary
            self.__buildHeap(freq_dict)
            # Build the Huffman tree from the heap
            self.__buildTree()
            # Build the Huffman codes from the tree
            self.__buildCodes()
            # Encode the text using the Huffman codes
            encoded_text = self.__getEncodedText(text)
            # Pad the encoded text
            padded_encoded_text = self.__getPaddedEncodedText(encoded_text)
            # Convert the padded encoded text to a byte array
            bytes_array = self.__getBytesArray(padded_encoded_text)
            # Write the byte array to the output file
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        
        print('Compressed')
        return output_path

    def __removePadding(self, text):
        # Remove padding from the encoded text
        padded_info = text[:8]
        extra_padding = int(padded_info, 2)
        text = text[8:]
        text_after_padding_removed = text[:-extra_padding]
        return text_after_padding_removed

    def __decodeText(self, text):
        # Decode the encoded text using the Huffman codes
        decoded_text = ""
        current_bits = ""
        for bit in text:
            current_bits += bit
            if current_bits in self.__reverseCodes:
                character = self.__reverseCodes[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text

    def decompress(self, input_path):
        # Decompress the file at the given path
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"
        
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # Read the compressed file and convert to a bit string
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            
            # Remove padding from the bit string
            actual_text = self.__removePadding(bit_string)
            # Decode the text using the Huffman codes
            decoded_text = self.__decodeText(actual_text)
            # Write the decoded text to the output file
            output.write(decoded_text)
        
        print('Decompressed')
        return output_path

path = '141.txt'
h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)
