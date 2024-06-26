# -*- coding: utf-8 -*-
"""ICP_Test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uysz_b392-CRNQy9JE53donPEM62XCGq
"""

# Environment Setup
import open3d as o3d
import numpy as np
import copy
import os
import sys

sys.path.append('..')

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

source = o3d.io.read_point_cloud("1716494961-351228219_LIDAR.pcd") # Read point cloud
target = o3d.io.read_point_cloud("1716494961-351228219_ZED.pcd") # Read point cloud
threshold = 0.02
trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
                         [-0.139, 0.967, -0.215, 0.7],
                         [0.487, 0.255, 0.835, -1.4],
                         [0.0, 0.0, 0.0, 1.0]])
draw_registration_result(source, target, trans_init)

"""Function evaluate_registration() calculates two main metrics:

1. fitness - measures the overlapping area. higher the better
2. inlier_rms - measures the RMSE of all inlier correspondences. lower the better
"""

# Initial Allignment
print("Initial alignment")
evaluation = o3d.pipelines.registration.evaluate_registration(source, target, threshold, trans_init)
print(evaluation)

"""Point-To-Point ICP"""
"""
reg_p2p = o3d.pipelines.registration.registration_icp(source, target, threshold, trans_init, o3d.pipelines.registration.TransformationEstimationPointToPoint()) # 30 Iterations
print(reg_p2p)
print("Transformation is:")
print(reg_p2p.transformation)
draw_registration_result(source, target, reg_p2p.transformation)"""

reg_p2p = o3d.pipelines.registration.registration_icp(source, target, threshold, trans_init, o3d.pipelines.registration.TransformationEstimationPointToPoint(),
                                                      o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=1000))
print(reg_p2p)
print("Transformation is:")
print(reg_p2p.transformation)
draw_registration_result(source, target, reg_p2p.transformation)

"""Point-To-Plane ICP"""

target.estimate_normals()
source.estimate_normals()
reg_p2l = o3d.pipelines.registration.registration_icp(source, target, threshold, trans_init, o3d.pipelines.registration.TransformationEstimationPointToPlane())
print(reg_p2l)
print("Transformation is:")
print(reg_p2l.transformation)
draw_registration_result(source, target, reg_p2l.transformation)
