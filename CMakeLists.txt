cmake_minimum_required(VERSION 2.8.3)
project(wearami_sockets)

find_package(catkin REQUIRED COMPONENTS message_generation
  rospy
  roscpp
  actionlib
)

catkin_package(
  CATKIN_DEPENDS
  rospy
  roscpp

)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#catkin_python_setup()


