"""
TODO:
1.根据文件夹读取video
2.根据文件夹存image
3.从文件夹下读、从txt读
4.frame name: folder + fid + pid
"""
import os
import argparse
import cv2
import json

parser = argparse.ArgumentParser(description='Get frame from video and save')
parser.add_argument('--skip', type=int, default=5, help="every n skip get one pic")
parser.add_argument('--save_root', type=str, default="/mnt/lustrenew/share/chenjinsheng/data/frame", help="data frame save root")
parser.add_argument('--json_root', type=str, default="/mnt/lustrenew/share/prediction/user/flj/projects/senseauto_sample/holstein/senseauto/build/sample/output_sr/object_recovery_result", help="data video save root")
parser.add_argument('--video_root', type=str, default="/mnt/lustre/share/AP_Recovery_Prediction/DATA_LJ/data/2018-08-01")

opt = parser.parse_args()

if __name__ == "__main__":
    if not os.path.exists(opt.video_root):
        raise ValueError("Wrong video root!!!")

    #if not os.path.exists(opt.save_root):
    #    os.mkdir(opt.save_root)

    # get folder name 
    folders = os.listdir(opt.video_root)
    for folder in folders:
        if folder.endswith("."):
            continue
        else:
            folder_name = os.path.join(opt.video_root, folder)
            json_path = os.path.join(opt.json_root, folder)
            fid = 0
            print("reading folder is: ", folder_name)

            # Get video
            video_name = os.path.join(folder_name, "CAM101.avi")
            if not os.path.exists(video_name):
                continue
            cap = cv2.VideoCapture(video_name)

            if not os.path.exists(json_name = os.path.join(json_path, "srresult-000000.json")):
                continue

            # Get frame image and json
            while cap.isOpened():
                status, image = cap.read()
                fid += 1
                if status:
                    json_name = os.path.join(json_path, "srresult-"+str(fid).zfill(6)+".json")
                    cars = json.load(open(json_name, 'r'))['vehicle_trajectory']
                    if len(cars) == 0:
                        continue
                    obj_num = len(cars)
                    for i in range(obj_num):
                        print("obj numbers are: ", obj_num)
                        obj = cars[i][0]['Object']
                        x = int(obj['bounding_box']['x'])
                        y = int(obj['bounding_box']['y'])
                        width = int(obj['bounding_box']['width'])
                        height = int(obj['bounding_box']['height'])
                        cropped_img = image[y:(y+height), x:(x+width)]

                        # save img
                        img_name = folder + '_' + str(obj['frame_index']) + '_' + str(obj['object_index']) + '.jpg'
                        if not os.path.exists(os.path.join(opt.save_root, folder)):
                            os.mkdir(os.path.join(opt.save_root, folder)) 
                        cv2.imwrite(os.path.join(opt.save_root, folder, img_name), cropped_img)

