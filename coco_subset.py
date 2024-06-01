import json
import json_understand as JView
import os
import shutil
#Goal: creat sub set of the whole dataset
#   (1)create new train.json 
#   (2)create new val.json 
#   (3)(optional) create new test.json
#       (1)make sure each file has images renamed 0-x

#(1) 
#   create list of desired categories.
#   create num of each category you want. same len array ^
#   load json object
#   Get at Anotations object and loop through all objects in it
#   test if category is a match with desire categories
#   If NO do nothing.
#   If Yes
#       save the image_id to a non repeating list
#       until you have the max for each category
#       save that annotation
#   Release annotation object in og json object

path_to_images = '../coco/images/val2017'
path_to_dump =''
path_to_dump = os.path.join(path_to_dump,'subset')

setup_sucess = True            
def load_json(file_path):
    if setup_sucess:
        with open(file_path, 'r') as file:
            return json.load(file)


desired_category_names = ["person","bird","cat","dog"]
desired_category_amounts = [150,100,100,100]
expected_num_imgs_to_keep = sum(desired_category_amounts)

if len(desired_category_amounts) != len(desired_category_names):
    print("*****ERROR: mismatch in lenght of desired categoris and amount per desiered categories.*****")
    desired_category_names = []
    desired_category_amounts = []
    setup_sucess = False

coco_json = load_json('../coco/annotations/instances_val2017.json')
JView.print_structure(coco_json)
desired_category_ids = []
desired_category_ids_to_names = {}
for category in coco_json["categories"]:
    if category["name"] in desired_category_names:
        category_id = category["id"]
        category_name = category["name"]
        desired_category_ids.append(category_id)
        desired_category_ids_to_names[category_id] = category_name
if len(desired_category_ids) != len(desired_category_names):
    setup_sucess = False
    print("*****ERROR: mismatch in length of desired categories and number of category ids to keep.*****")
print(f"Category IDs to keep: {desired_category_ids}")


ids_of_imgs_to_keep = set()
old_img_ids_to_new = {}
annotations_to_keep = []
for annotation in coco_json["annotations"]:
    if annotation["category_id"] in desired_category_ids:
        category_id = annotation['category_id']
        category_name = desired_category_ids_to_names[category_id]
        category_name_index = desired_category_names.index(category_name)

        if desired_category_amounts[category_name_index] > 0:
            annotations_to_keep
            if annotation["image_id"] not in ids_of_imgs_to_keep:
                ids_of_imgs_to_keep.add(annotation["image_id"])
                desired_category_amounts[category_name_index] -= 1
                old_img_ids_to_new[annotation["image_id"]] = len(old_img_ids_to_new)
        #Is this an annotation that we are keeping? 
        if annotation["image_id"] in ids_of_imgs_to_keep:
            #Store and prep annottion for new .json file
            annotation['image_id'] = old_img_ids_to_new[annotation["image_id"]]
            annotation['id'] = len(annotations_to_keep)
            annotation['category_id'] = category_name_index
            annotations_to_keep.append(annotation)
#New Annotations finished.
del coco_json["annotations"]
print
print(f"Total Images To Keep: {len(ids_of_imgs_to_keep)}")
print(f"Expected: {expected_num_imgs_to_keep}")
print("Total Amounts Left Per Category:")
print(desired_category_amounts)
print("New img IDs from old ones:")
# for old in old_img_ids_to_new:
#     print(f"{old_img_ids_to_new[old]} <== {old}")
# print("^^^ New img IDs from old ones ^^^")


images_to_keep = []


#   Get at coco.json images key-value:pair 
#       get rid off all non-keeping image objecst
#       prep all keeping image objects
old_img_file_names_to_new = {}
for image in coco_json["images"]:
    if image["id"] in ids_of_imgs_to_keep:
        image["id"] = old_img_ids_to_new [image["id"]]
        old_file_name = image['file_name']
        file_extension = old_file_name.split('.')[-1]
        new_file_name = f"{image['id']}.{file_extension}"
        image['file_name'] = new_file_name
        old_img_file_names_to_new[old_file_name] = new_file_name
        images_to_keep.append(image)
#done processing the images section to keep for new .json file
del coco_json["images"]
print(f"Images Actually Kept Amount: {len(images_to_keep)}")

#Get at Categories of coco json object
#   keep only desired categries 
#   rename category IDs based on desired categories array index
categories_to_keep = []
for category in coco_json["categories"]:
    if category["name"] in desired_category_names:
        category["id"] = desired_category_names.index(category["name"])
        categories_to_keep.append(category)
#Categoreis to keep for new .json done
del coco_json['categories']

new_json = coco_json
coco_json = {}

new_json["images"] = images_to_keep
new_json["annotations"] = annotations_to_keep
new_json["categories"] = categories_to_keep




#Have: old_img_file_names_to_new dictionary
#   rename images

path_to_new__imgs_dir = os.path.join(path_to_dump,'images')
os.makedirs(path_to_new__imgs_dir, exist_ok=True)

for filename in os.listdir(path_to_images):
    if filename in old_img_file_names_to_new:
        new_filename = old_img_file_names_to_new[filename]

        original_file_path = os.path.join(path_to_images, filename)
        new_file_path = os.path.join(path_to_new__imgs_dir, new_filename)

        shutil.copy2(original_file_path, new_file_path)
        print(f"Copied '{filename}' to '{new_filename}'")

print("All specified files have been copied.")

#   create json categories with only desired categories
#       remap cat_ids accoring to desired array
#   create new json object and save it

new_json_path = os.path.join(path_to_dump,'annotaions.json')
with open(new_json_path, 'w') as file:
    #json.dump(new_json, file)
    json.dump(new_json, file, indent=4)

##future improvments
"""
oragnize paths an requre user to just give dump file wher everyhing wil be dumped.
    the .json file will be named the same as the old file by defoult

allow user to give new names for json file and image file.

allow for 2 datasets to be added at once
make the images secontion of json and annotations in order of images

make prints optional for debuging. or create logging function.

allow to be run from CLI

allow for user to not copy over ceretain data such as segmentation data

fix bounding boxes or verify that it s correct

"""


