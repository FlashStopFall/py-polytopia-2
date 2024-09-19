from PIL import Image 

mapSize = 11
pixelsPerSquare = 16
# Create an image as input: 
input_image = Image.new(mode="RGB", size=(mapSize*pixelsPerSquare, mapSize*pixelsPerSquare), 
                        color="white") 

"""  
# save the image as "input.png" 
#(not mandatory) 
input_image.save("input", format="png") """
  
# Extracting pixel map: 
pixel_map = input_image.load() 
  
# Extracting the width and height 
# of the image: 
width, height = input_image.size 


#make a grid of only edges
for i in range(mapSize):
    for j in range(mapSize):
        
        for x in range(pixelsPerSquare):
            for y in range(pixelsPerSquare):
                
                if x==0 or x==15 or y==0 or y==15:
                    pixel_map[(i*16)+x, (j*16)+y] = (50, 50, 50)

                else:
                    pixel_map[(i*16)+x, (j*16)+y] = (150, 150, 150)

  
# Saving the final output 
# as "output.png": 
input_image.save("output.png", format="png") 

input_image.show()
# use input_image.show() to see the image on the 
# output screen. 
