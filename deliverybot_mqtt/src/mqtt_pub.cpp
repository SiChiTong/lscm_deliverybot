#include <memory>
#include <chrono>
#include <functional>

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
        : Node("minimal_subscriber")
    {
        status_pub_ = this->create_publisher<deliverybot_mqtt::msg::Status>("robots/status", 10);
        location_pub_ = this->create_publisher<deliverybot_mqtt::msg::Location>("robots/location", 10);
        config_pub_ = this->create_publisher<deliverybot_mqtt::msg::Configuration>("robots/configuration", 10);

        timer_ = this->create_wall_timer(1000ms, std::bind(&MqttNode::timer_callback, this));

        subscription_ = this->create_subscription<geometry_msgs::msg::PoseWithCovarianceStamped>(
            "amcl_pose", 10, std::bind(&MqttNode::location_callback, this, _1));
    }

private:
    void location_callback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg) const
    {
        // Location publisher
        auto location = deliverybot_mqtt::msg::Location();
        location.pose = msg->pose.pose;
        location.map = "testmap";
        location_pub_->publish(location);
    }

    void timer_callback()
    {
        // Configuration publisher
        auto config = deliverybot_mqtt::msg::Configuration();
        auto location_entry = deliverybot_mqtt::msg::LocationEntry();
        config.robot_id = 1;
        for (int i = 0; i < 2; i++)
        {
            location_entry.id = i;
            location_entry.name = "A";
            location_entry.pose.position.x = i;
            config.location.push_back(location_entry);
        }
        config_pub_->publish(config);

        // Status publisher
        auto status = deliverybot_mqtt::msg::Status();
        status.id = 1;
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