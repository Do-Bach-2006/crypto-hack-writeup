from PIL import Image
import numpy as np

# Open the two XOR encrypted images
img1 = Image.open('flag_7ae18c704272532658c10b5faad06d74.png')
img2 = Image.open('lemur_ed66878c338e662d3473f0d98eedbd0d.png')

# Convert images to numpy arrays
arr1 = np.array(img1)
arr2 = np.array(img2)

# XOR the RGB bytes
result_arr = np.bitwise_xor(arr1, arr2)

# Convert back to Image and save
result_img = Image.fromarray(result_arr)
result_img.save('result.png')

print("Saved XOR result to result.png")
