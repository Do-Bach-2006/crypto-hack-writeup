import idaapi
import idc
import idautils

# ==============================================================
# IDAPYTHON REVERSE ENGINEERING CHEATSHEET
# Run this inside IDA Pro via "File -> Script Command" or CLI
# ==============================================================

# --- 1. Basic Navigation and Information ---
# Get the current cursor address
curr_addr = idc.here()
print(f"Current address: {hex(curr_addr)}")

# Go to a specific address or function name in the IDA View
idc.jumpto(0x401000)
# idc.jumpto(idc.get_name_ea_simple("main"))

# --- 2. Renaming and Commenting ---
# Rename a variable or function at a specific address
address = 0x401000
idc.set_name(address, "my_custom_function_name")

# Add a comment (1 = repeatable comment, 0 = regular)
idc.set_cmt(curr_addr, "Vulnerable strcpy here!", 0)

# --- 3. Patching Bytes ---
# Useful for skipping anti-debugging checks or patching out loops
patch_addr = 0x401050

# Read current byte/word/dword
original_byte = idc.get_wide_byte(patch_addr)
# Patch with NOPs (0x90 for x86/x64 architecture)
idc.patch_byte(patch_addr, 0x90)
idc.patch_byte(patch_addr + 1, 0x90)

# --- 4. Cross References (Xrefs) ---
# Find all places where a function or variable is called/used
target_func = idc.get_name_ea_simple("strcpy")

print("strcpy is called from:")
for xref in idautils.XrefsTo(target_func):
    print(f"- {hex(xref.frm)}")

# --- 5. Iterating through Functions and Instructions ---
# Loop over all known functions in the binary
for func in idautils.Functions():
    func_name = idc.get_func_name(func)
    # print(f"Function {func_name} at {hex(func)}")

# Loop over all instructions within the currently selected function
# Try to safely get the current function block
func_t = idaapi.get_func(curr_addr)
if func_t:
    func_start = func_t.start_ea
    func_end = func_t.end_ea

    for head in idautils.Heads(func_start, func_end):
        # Print the instruction assembly e.g. "mov eax, 1"
        disasm = idc.generate_disasm_line(head, 0)
        # print(f"{hex(head)}: {disasm}")

# --- 6. Reading and Extracting Data ---
# Read extracted bytes from a `.data` or `.rodata` section
data_start = 0x403000
data_len = 100
extracted_bytes = idc.get_bytes(data_start, data_len)
# You can then use it in your crypto decryption algorithms!

# --- 7. Colorizing Blocks and Instructions ---
# Color highlight a specific instruction to make analyzing control flow easier
# Colors are BBGGRR (Blue Green Red) hex format
highlight_color = 0x00A0FF # Light Orange/Brown
idc.set_color(curr_addr, idc.CIC_ITEM, highlight_color)

# To remove a color:
# idc.set_color(curr_addr, idc.CIC_ITEM, 0xFFFFFFFF)
