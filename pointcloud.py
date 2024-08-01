import open3d as o3d
import numpy as np

# LiDAR 데이터 로드
pcd = o3d.io.read_point_cloud("경로.pcd")

# 포인트 클라우드 정보 출력
points = np.asarray(pcd.points)
print("전체 포인트 수:", points.shape[0])
print("포인트 범위 (X):", points[:, 0].min(), "to", points[:, 0].max())
print("포인트 범위 (Y):", points[:, 1].min(), "to", points[:, 1].max())
print("포인트 범위 (Z):", points[:, 2].min(), "to", points[:, 2].max())

# ROI 정의 (예: 특정 x, y, z 범위)
# x_min, x_max = -22559, 19623
# y_min, y_max = -35875, 47274
# z_min, z_max = 0, 39269

x_min, x_max = -7000, 13000
y_min, y_max = -18000, 1500
z_min, z_max = 20000, 39269

# 관심 영역 필터링
roi_indices = np.where(
    (points[:, 0] >= x_min) & (points[:, 0] <= x_max) &
    (points[:, 1] >= y_min) & (points[:, 1] <= y_max) &
    (points[:, 2] >= z_min) & (points[:, 2] <= z_max)
)[0]

# 관심 영역의 포인트만 선택
roi_pcd = pcd.select_by_index(roi_indices)

# 필터링된 포인트의 수 출력
filtered_points = np.asarray(roi_pcd.points)
print("필터링된 포인트 수:", filtered_points.shape[0])

# 시각화 창 설정
vis = o3d.visualization.Visualizer()
vis.create_window(window_name='LiDAR Point Cloud', width=800, height=600, left=50, top=50)
vis.add_geometry(roi_pcd)

# 카메라 뷰 설정
view_control = vis.get_view_control()
view_control.set_zoom(0.8)  # 줌 레벨 조정
view_control.set_front([0.0, 0.0, -1.0])
view_control.set_lookat([0.0, 0.0, 0.0])
view_control.set_up([0.0, -1.0, 0.0])

# 시각화 시작
vis.run()

# 시각화 종료
vis.destroy_window()

# 선택된 관심 영역을 PCD 파일로 저장
o3d.io.write_point_cloud("roi_lidar_data.pcd", roi_pcd)

# 필터링된 포인트 클라우드의 범위 출력
print("ROI 포인트 범위 (X):", filtered_points[:, 0].min(), "to", filtered_points[:, 0].max())
print("ROI 포인트 범위 (Y):", filtered_points[:, 1].min(), "to", filtered_points[:, 1].max())
print("ROI 포인트 범위 (Z):", filtered_points[:, 2].min(), "to", filtered_points[:, 2].max())
