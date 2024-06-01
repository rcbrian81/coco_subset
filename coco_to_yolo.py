import os 
import json

name_of_annotation_file = 'annotaions.json'
path_to_data_set = 'coco_subset/subset/'

path_to_images = os.path.join(path_to_data_set,'images/')
path_to_dump = 'new_yolo_data_set'
path_to_labels = os.path.join(path_to_dump,'labels')
path_to_annotation_file = os.path.join(path_to_data_set,name_of_annotation_file)

print(path_to_annotation_file)
with open(path_to_annotation_file,'r') as file:
	coco_json = json.load(file)

images = coco_json.pop('images')
annotations = coco_json.pop('annotations')
categories = coco_json.pop('categories')
del coco_json


images_dic = {}
for image in images:
	images_dic[image['id']] = image
del images

if not os.path.exists(path_to_dump):
    os.makedirs(path_to_dump)
if not os.path.exists(path_to_labels):
    os.makedirs(path_to_labels)

for annotation in annotations:
	image_id = annotation["image_id"]
	image_file_name = images_dic[image_id]['file_name']
	txt_file_name = os.path.splitext(image_file_name)[0] + '.txt'
	path_to_txt_file = os.path.join(path_to_labels,txt_file_name)

	image_width = images_dic[image_id]['width']
	image_height = images_dic[image_id]['height']

	old_x = annotation["bbox"][0]
	old_y = annotation["bbox"][1]
	old_width = annotation["bbox"][2]
	old_height = annotation["bbox"][3]

	x = (old_x + (.5*old_width))/image_width
	y = (old_y + (.5*old_height))/image_height
	width = old_width/image_width
	height = old_height/image_height
	annotation_line = f"{annotation['category_id']} {x} {y} {width} {height}\n"
	with open(path_to_txt_file,'a') as file:
		file.write(annotation_line)
"""
Create text files for each image
	Loop thorugh annotations and loock at the image_id
	Look up its file name.
	If you havnet seen it before
		create text file with the same name. 
	Get the annotations bb and conver it to a Yolo bb
	Open .txt file with the same name
	store in the information on a new line. category_id, x, y , widht, height
"""








