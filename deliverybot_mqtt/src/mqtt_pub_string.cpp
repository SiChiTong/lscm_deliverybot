#include <memory>
#include <chrono>
#include <functional>
#include <string.h>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
#include "std_msgs/msg/string.hpp"
#include "deliverybot_mqtt_interfaces/msg/status.hpp"
#include "deliverybot_mqtt_interfaces/msg/location.hpp"
#include "deliverybot_mqtt_interfaces/msg/location_entry.hpp"
// #include "deliverybot_mqtt_interfaces/msg/configuration.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

class MqttNode : public rclcpp::Node
{
public:
    MqttNode()
        : Node("mqtt_node")
    {
        // declare params
        this->declare_parameter("robot_id", rclcpp::PARAMETER_INTEGER);
        this->declare_parameter("num_of_locations", rclcpp::PARAMETER_INTEGER);
        this->declare_parameter("location.location_id", rclcpp::PARAMETER_INTEGER_ARRAY);
        this->declare_parameter("location.location_name", rclcpp::PARAMETER_STRING_ARRAY);
        this->declare_parameter("location.coordinate_x", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.coordinate_y", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.orientation_z", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.orientation_w", rclcpp::PARAMETER_DOUBLE_ARRAY);

        rclcpp::Parameter robot_id = this->get_parameter("robot_id");
        status_pub_ = this->create_publisher<std_msgs::msg::String>("robots/id_" + std::to_string(robot_id.as_int()) + "/status", 10);
        location_pub_ = this->create_publisher<std_msgs::msg::String>("robots/id_" + std::to_string(robot_id.as_int()) + "/location", 10);
        config_pub_ = this->create_publisher<std_msgs::msg::String>("robots/configuration", 10);

        timer_ = this->create_wall_timer(1000ms, std::bind(&MqttNode::timer_callback, this));

        amcl_sub_ = this->create_subscription<geometry_msgs::msg::PoseWithCovarianceStamped>(
            "amcl_pose", 10, std::bind(&MqttNode::location_callback, this, _1));
        status_sub_ = this->create_subscription<deliverybot_mqtt_interfaces::msg::Status>(
            "status", 10, std::bind(&MqttNode::status_callback, this, _1));
    }

private:
    double robot_pose[7] = {};
    struct
    {
        int robot_id;
        std::string status = "WAITING";
        int from_id = 1;
        int to_id = 1;
    } status_struct;

    void
    status_callback(const deliverybot_mqtt_interfaces::msg::Status::SharedPtr msg)
    {
        status_struct.status = msg->status;
        status_struct.from_id = msg->from_location_id;
        status_struct.to_id = msg->to_location_id;
    }

    void location_callback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg)
    {
        // save location in local array
        robot_pose[0] = msg->pose.pose.position.x;
        robot_pose[1] = msg->pose.pose.position.y;
        robot_pose[5] = msg->pose.pose.orientation.z;
        robot_pose[6] = msg->pose.pose.orientation.w;

        // location_pub_->publish(location);
    }

    void timer_callback()
    {
        rclcpp::Parameter robot_id = this->get_parameter("robot_id");
        rclcpp::Parameter num_of_locations = this->get_parameter("num_of_locations");
        rclcpp::Parameter location_id = this->get_parameter("location.location_id");
        rclcpp::Parameter location_name = this->get_parameter("location.location_name");
        rclcpp::Parameter coordinate_x = this->get_parameter("location.coordinate_x");
        rclcpp::Parameter coordinate_y = this->get_parameter("location.coordinate_y");
        rclcpp::Parameter orientation_w = this->get_parameter("location.orientation_z");
        rclcpp::Parameter orientation_z = this->get_parameter("location.orientation_w");
        // Configuration publisher
        auto config_ros = std_msgs::msg::String();
        std::string config = "{\"robot_id\":" + std::to_string(robot_id.as_int());
        auto location_entry = std_msgs::msg::String();
        config.append(",\"location\":[");
        for (int i = 0; i < num_of_locations.as_int(); i++)
        {
            config.append("{\"id\":" + std::to_string(location_id.as_integer_array()[i]));
            config.append(",\"name\":\"" + location_name.as_string_array()[i] + "\"");
            config.append(",\"pose\":{\"position\":{\"x\":" + std::to_string(coordinate_x.as_double_array()[i]) + ",\"y\":");
            config.append(std::to_string(coordinate_y.as_double_array()[i]) + ",\"z\":");
            config.append("0.000000}");
            config.append(",\"orientation\":{\"x\":0.000000,\"y\":0.000000,\"z\":");
            config.append(std::to_string(orientation_w.as_double_array()[i]) + ",\"w\":");
            config.append(std::to_string(orientation_z.as_double_array()[i]) + "}");
            config.append("}},");
        }
        config.pop_back(); // remove the last character ","
        config.append("]}");
        config_ros.data = config;
        config_pub_->publish(config_ros);

        // Status publisher
        auto status_ros = std_msgs::msg::String();
        std::string status = "{\"robot_id\":" + std::to_string(robot_id.as_int());
        status.append(",\"status\":\"" + status_struct.status + "\"");
        status.append(",\"battery_remaining\":56");
        status.append(",\"from_location_id\":" + std::to_string(status_struct.from_id));
        status.append(",\"to_location_id\":" + std::to_string(status_struct.to_id));
        status.append("}");
        status_ros.data = status;
        status_pub_->publish(status_ros);

        // Location publisher
        auto location_ros = std_msgs::msg::String();
        std::string location = "{\"pose\":{\"position\":{\"x\":" + std::to_string(robot_pose[0]);
        location.append(",\"y\":" + std::to_string(robot_pose[1]));
        location.append(",\"z\":0.000000},\"orientation\":{\"x\":0.000000,\"y\":0.000000");
        location.append(",\"z\":" + std::to_string(robot_pose[5]));
        location.append(",\"w\":" + std::to_string(robot_pose[6]));
        location.append("}}}");
        location_ros.data = location;
        location_pub_->publish(location_ros);
    }
    rclcpp::TimerBase::SharedPtr timer_;

    rclcpp::Subscription<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr amcl_sub_;
    rclcpp::Subscription<deliverybot_mqtt_interfaces::msg::Status>::SharedPtr status_sub_;

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr location_pub_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr config_pub_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MqttNode>());
    rclcpp::shutdown();
    return 0;
}