cmake_minimum_required(VERSION 3.5)
project(inverse_kine)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
find_package(inverse_kine REQUIRED)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/XyzToJoints.srv"
  "msg/JointsRad.msg"
 )
 
 add_executable(xyzToJointsServer src/xyzToJointsServer.cpp)
 ament_target_dependencies(xyzToJointsServer rclcpp inverse_kine)

 install(TARGETS
 xyzToJointsServer
 DESTINATION lib/${PROJECT_NAME}
 )

ament_package()
