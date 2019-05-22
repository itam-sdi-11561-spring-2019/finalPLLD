#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include <std_msgs/Int32.h>

#define RATE_HZ 2

using namespace std;

ros::Publisher velocity_publisher;

void move(double speed, double distance, bool isForward);

int main(int argc, char **argv)
{
	ros::init(argc, argv, "tortu_node");
	ros::NodeHandle nh;
	ros::Publisher pub = nh.advertise<geometry_msgs::Twist> ("/turtle1/cmd_vel", 10);
	ros::Subscriber sub_vel = nh.subscribe("/msg_respuesta", 1000, &get_msg);
	ros::Rate rate(RATE_HZ);
	geometry_msgs::Twist msg;
	std_msgs::String instruccion;

	while (ros::ok())
	{
		cout << "Introduce una instrucción:" << endl;
		cin >> instruccion;

		if (instruccion == 2){
			msg = 
		}
		
		pub.publish(msg);

		ROS_INFO_STREAM(".");

		ros::spinOnce();
		rate.sleep();
	}

    return 0;
}