#include <memory>
#include <chrono>
#include <functional>
#include <string.h>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
#include "deliverybot_mqtt/msg/status.hpp"
#include "deliverybot_mqtt/msg/location.hpp"
#include "deliverybot_mqtt/msg/location_entry.hpp"
#include "deliverybot_mqtt/msg/configuration.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

class MqttNode : public rclcpp::Node
{
public:
    MqttNode()
        : Node("mqtt_node")
    {
        // declare params
        this->declare_parameter("map", rclcpp::PARAMETER_STRING);
        this->declare_parameter("robot_id", rclcpp::PARAMETER_INTEGER);
        this->declare_parameter("num_of_locations", rclcpp::PARAMETER_INTEGER);
        this->declare_parameter("location.location_id", rclcpp::PARAMETER_INTEGER_ARRAY);
        this->declare_parameter("location.location_name", rclcpp::PARAMETER_STRING_ARRAY);
        this->declare_parameter("location.coordinate_x", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.coordinate_y", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.orientation_z", rclcpp::PARAMETER_DOUBLE_ARRAY);
        this->declare_parameter("location.orientation_w", rclcpp::PARAMETER_DOUBLE_ARRAY);

        rclcpp::Parameter robot_id = this->get_parameter("robot_id");
        status_pub_ = this->create_publisher<deliverybot_mqtt::msg::Status>("robots/id_" + std::to_string(robot_id.as_int()) + "/status", 10);
        location_pub_ = this->create_publisher<deliverybot_mqtt::msg::Location>("robots/id_" + std::to_string(robot_id.as_int()) + "/location", 10);
        config_pub_ = this->create_publisher<deliverybot_mqtt::msg::Configuration>("robots/configuration", 10);

        rclcpp::Parameter num_of_locations = this->get_parameter("num_of_locations");
        rclcpp::Parameter location_id = this->get_parameter("location.location_id");
        rclcpp::Parameter location_name = this->get_parameter("location.location_name");
        rclcpp::Parameter coordinate_x = this->get_parameter("location.coordinate_x");
        rclcpp::Parameter coordinate_y = this->get_parameter("location.coordinate_y");
        rclcpp::Parameter orientation_w = this->get_parameter("location.orientation_z");
        rclcpp::Parameter orientation_z = this->get_parameter("location.orientation_w");
        // Configuration publisher
        auto config = deliverybot_mqtt::msg::Configuration();
        auto location_entry = deliverybot_mqtt::msg::LocationEntry();
        config.robot_id = robot_id.as_int();
        for (int i = 0; i < num_of_locations.as_int(); i++)
        {
            location_entry.id = location_id.as_integer_array()[i];
            location_entry.name = location_name.as_string_array()[i];
            location_entry.pose.position.x = coordinate_x.as_double_array()[i];
            location_entry.pose.position.y = coordinate_y.as_double_array()[i];
            location_entry.pose.orientation.z = orientation_z.as_double_array()[i];
            location_entry.pose.orientation.w = orientation_w.as_double_array()[i];
            config.location.push_back(location_entry);
        }
        config_pub_->publish(config);

        timer_ = this->create_wall_timer(1000ms, std::bind(&MqttNode::timer_callback, this));

        subscription_ = this->create_subscription<geometry_msgs::msg::PoseWithCovarianceStamped>(
            "amcl_pose", 10, std::bind(&MqttNode::location_callback, this, _1));
    }

private:
    void location_callback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg) const
    {
        rclcpp::Parameter map = this->get_parameter("map");
        // Location publisher
        auto location = deliverybot_mqtt::msg::Location();
        location.pose = msg->pose.pose;
        location.map = map.as_string();
        location_pub_->publish(location);
    }

    void timer_callback()
    {
        rclcpp::Parameter robot_id = this->get_parameter("robot_id");
        // rclcpp::Parameter num_of_locations = this->get_parameter("num_of_locations");
        // rclcpp::Parameter location_id = this->get_parameter("location.location_id");
        // rclcpp::Parameter location_name = this->get_parameter("location.location_name");
        // rclcpp::Parameter coordinate_x = this->get_parameter("location.coordinate_x");
        // rclcpp::Parameter coordinate_y = this->get_parameter("location.coordinate_y");
        // rclcpp::Parameter orientation_w = this->get_parameter("location.orientation_z");
        // rclcpp::Parameter orientation_z = this->get_parameter("location.orientation_w");
        // // Configuration publisher
        // auto config = deliverybot_mqtt::msg::Configuration();
        // auto location_entry = deliverybot_mqtt::msg::LocationEntry();
        // config.robot_id = robot_id.as_int();
        // for (int i = 0; i < num_of_locations.as_int(); i++)
        // {
        //     location_entry.id = location_id.as_integer_array()[i];
        //     location_entry.name = location_name.as_string_array()[i];
        //     location_entry.pose.position.x = coordinate_x.as_double_array()[i];
        //     location_entry.pose.position.y = coordinate_y.as_double_array()[i];
        //     location_entry.pose.orientation.z = orientation_z.as_double_array()[i];
        //     location_entry.pose.orientation.w = orientation_w.as_double_array()[i];
        //     config.location.push_back(location_entry);
        // }
        // config_pub_->publish(config);

        // Status publisher
        auto status = deliverybot_mqtt::msg::Status();
        status.robot_id = robot_id.as_int();
        status.status = "PROCESSING";
        status.battery_remaining = 56;
        status.from_location_id = 1;
        status.to_location_id = 2;
        status_pub_->publish(status);
    }
    rclcpp::TimerBase::SharedPtr timer_;

    rclcpp::Subscription<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr subscription_;

    rclcpp::Publisher<deliverybot_mqtt::msg::Status>::SharedPtr status_pub_;
    rclcpp::Publisher<deliverybot_mqtt::msg::Location>::SharedPtr location_pub_;
    rclcpp::Publisher<deliverybot_mqtt::msg::Configuration>::SharedPtr config_pub_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MqttNode>());
    rclcpp::shutdown();
    return 0;
}