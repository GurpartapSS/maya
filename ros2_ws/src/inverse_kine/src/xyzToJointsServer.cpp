#include "rclcpp/rclcpp.hpp"
#include "inverse_kine/srv/xyz_to_joints.hpp"
// #include "inverse_kine/inverse_kine_util.hpp"
#include<vector>
class ik
{
public:
    ik(int j1, int j2) : j1_(j1), j2_(j2), orientation_(0)
    {
    }
    // h - height, d - depth, y - position on floor
    // return: m1 - b_static in XY, m2 - a1 in YZ, m3 - a2 in YZ, m4 - orientation in in YZ, please follow the reference image
    std::vector<float> convert(double h, double y, double d)
    {
        std::vector<float> port;
        float raise_base = sqrt(d*d + h*h);
        float m1_adj = atan2(h, d);                                                  // angle by which the triangle is lifted
        port.push_back(atan2(y, d));                                                 // m1 - movement of base along the floor left/right
        port.push_back(M_PI / 2 - getAngle(j1_, raise_base, j2_) - m1_adj);          // m2 - angle to move from 90deg rest position, front/back 
        port.push_back(M_PI - getAngle(j1_, j2_, raise_base));                       // m3 - angle to move wrt arm1 rest alignment, front/back
        float wrist_adj = getAngle(j2_, raise_base, j1_) - (M_PI/2 - atan2(d,h)); 
        port.push_back(wrist_adj);                                      // m4 - angle to move wrt arm2 keeping horizzontal alignment, up/down

        return port;
    }

private:
    int j1_;          // length1
    int j2_;          // length2
    int orientation_; // position wrt obj, 0 is standing
    static const int hand_ca = 0;

    float getAngle(double a, double b, double op)
    {
        return acos(((a * a) + (b * b) - (op * op)) / (2 * a * b));
    }
};

class xyzToJointsServer : public rclcpp::Node
{
public:
    xyzToJointsServer() : Node("xyz_to_joints_server"), converter_(12,12)
    {
        server_ = this->create_service<inverse_kine::srv::XyzToJoints>("xyz_to_joints",
                                                                  std::bind(&xyzToJointsServer::callbackAddTwoInts, 
                                                                  this, std::placeholders::_1, std::placeholders::_2));
        RCLCPP_INFO(this->get_logger(),"Service Server Started");
    }

private:
    rclcpp::Service<inverse_kine::srv::XyzToJoints>::SharedPtr server_;
    ik converter_;
    void callbackAddTwoInts(const inverse_kine::srv::XyzToJoints::Request::SharedPtr request_,
                            const inverse_kine::srv::XyzToJoints::Response::SharedPtr response_)
    {
        RCLCPP_INFO(this->get_logger(),"New Request received!");
        std::vector<float> joints = converter_.convert(request_->h,request_->y,request_->d);
        response_->joints = joints;
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<xyzToJointsServer>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}