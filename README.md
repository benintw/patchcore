### 1. 把分割好的資料（良好的）放到資料夾 'nominal_processed_by_hugo'

### 2. `split_data()` 會用資料夾 'nominal_processed_by_hugo'做:

- 建立資料夾:
  - 'training_imgs'
  - 'testing_imgs/defect'
  - 'testing_imgs/good'
- 把良好的照片分成 9:1，把 9 放到資料夾'training_img'
- 把剩下的 1 放到資料夾'testing_img'底下的'good'子資料夾
- 然後從'nominal_processed_by_hugo'隨機選 10%的照片檔案，並隨機位置的夾上隨機 1 ～ 5 個黑點或白點，之後放到‘testing_img'底下的'defect'子資料夾
