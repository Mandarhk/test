#include <opencv2/opencv.hpp>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.hpp"

class ImageProjector : public rclcpp::Node {
public:
    ImageProjector() : Node("image_projector") {
        subscriber_ = this->create_subscription<sensor_msgs::msg::Image>(
            "/image_raw", 10, std::bind(&ImageProjector::image_callback, this, std::placeholders::_1));
        RCLCPP_INFO(this->get_logger(), "Image projector node has started and subscribed to /usb_cam/image_raw.");
    }

private:
    void image_callback(const sensor_msgs::msg::Image::SharedPtr msg) {
        cv_bridge::CvImagePtr cv_ptr;
        try {
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
            auto image = cv_ptr->image;

            // Project the points onto the RGB image
            std::vector<cv::Point2f> points_2d = project_points();
            for (auto & point : points_2d) {
                cv::circle(image, point, 5, CV_RGB(0, 255, 0), -1);
            }

            cv::imshow("Projected Image", image);
            cv::waitKey(1);
            RCLCPP_INFO(this->get_logger(), "Processed an image frame and displayed the projected points.");

        } catch (cv_bridge::Exception& e) {
            RCLCPP_ERROR(this->get_logger(), "Could not convert from '%s' to 'bgr8'. Error: %s", msg->encoding.c_str(), e.what());
        }
    }

    std::vector<cv::Point2f> project_points() {
        std::vector<cv::Point3f> points_3d = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        std::vector<cv::Point2f> points_2d;
        cv::Mat camera_matrix = (cv::Mat_<double>(3, 3) << 969.6953825243171, 0, 655.1533584594727, 0, 969.6953825243171, 360.8238639831543, 0, 0, 1);
        cv::Mat dist_coeffs = (cv::Mat_<double>(1, 5) << -0.0551288, -0.0703789, 0, 9.76616e-05, 0.000108951);

        cv::projectPoints(points_3d, cv::Vec3f(0,0,0), cv::Vec3f(0,0,0), camera_matrix, dist_coeffs, points_2d);
        return points_2d;
    }

    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscriber_;
};

int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ImageProjector>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
