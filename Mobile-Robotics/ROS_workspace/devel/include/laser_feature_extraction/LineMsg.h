// Generated by gencpp from file laser_feature_extraction/LineMsg.msg
// DO NOT EDIT!


#ifndef LASER_FEATURE_EXTRACTION_MESSAGE_LINEMSG_H
#define LASER_FEATURE_EXTRACTION_MESSAGE_LINEMSG_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geometry_msgs/Point.h>
#include <geometry_msgs/Point.h>

namespace laser_feature_extraction
{
template <class ContainerAllocator>
struct LineMsg_
{
  typedef LineMsg_<ContainerAllocator> Type;

  LineMsg_()
    : A(0.0)
    , B(0.0)
    , C(0.0)
    , p_a()
    , p_b()
    , id(0)  {
    }
  LineMsg_(const ContainerAllocator& _alloc)
    : A(0.0)
    , B(0.0)
    , C(0.0)
    , p_a(_alloc)
    , p_b(_alloc)
    , id(0)  {
  (void)_alloc;
    }



   typedef double _A_type;
  _A_type A;

   typedef double _B_type;
  _B_type B;

   typedef double _C_type;
  _C_type C;

   typedef  ::geometry_msgs::Point_<ContainerAllocator>  _p_a_type;
  _p_a_type p_a;

   typedef  ::geometry_msgs::Point_<ContainerAllocator>  _p_b_type;
  _p_b_type p_b;

   typedef int32_t _id_type;
  _id_type id;





  typedef boost::shared_ptr< ::laser_feature_extraction::LineMsg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::laser_feature_extraction::LineMsg_<ContainerAllocator> const> ConstPtr;

}; // struct LineMsg_

typedef ::laser_feature_extraction::LineMsg_<std::allocator<void> > LineMsg;

typedef boost::shared_ptr< ::laser_feature_extraction::LineMsg > LineMsgPtr;
typedef boost::shared_ptr< ::laser_feature_extraction::LineMsg const> LineMsgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::laser_feature_extraction::LineMsg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace laser_feature_extraction

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/melodic/share/sensor_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg'], 'laser_feature_extraction': ['/home/turtlebot/ros_workspace/src/laser_feature_extraction/msg'], 'visualization_msgs': ['/opt/ros/melodic/share/visualization_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::laser_feature_extraction::LineMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::laser_feature_extraction::LineMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::laser_feature_extraction::LineMsg_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "13328a699d80bf05ec8bf826fc92406c";
  }

  static const char* value(const ::laser_feature_extraction::LineMsg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x13328a699d80bf05ULL;
  static const uint64_t static_value2 = 0xec8bf826fc92406cULL;
};

template<class ContainerAllocator>
struct DataType< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "laser_feature_extraction/LineMsg";
  }

  static const char* value(const ::laser_feature_extraction::LineMsg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 A\n\
float64 B\n\
float64 C\n\
geometry_msgs/Point p_a\n\
geometry_msgs/Point p_b\n\
int32 id\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Point\n\
# This contains the position of a point in free space\n\
float64 x\n\
float64 y\n\
float64 z\n\
";
  }

  static const char* value(const ::laser_feature_extraction::LineMsg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.A);
      stream.next(m.B);
      stream.next(m.C);
      stream.next(m.p_a);
      stream.next(m.p_b);
      stream.next(m.id);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct LineMsg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::laser_feature_extraction::LineMsg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::laser_feature_extraction::LineMsg_<ContainerAllocator>& v)
  {
    s << indent << "A: ";
    Printer<double>::stream(s, indent + "  ", v.A);
    s << indent << "B: ";
    Printer<double>::stream(s, indent + "  ", v.B);
    s << indent << "C: ";
    Printer<double>::stream(s, indent + "  ", v.C);
    s << indent << "p_a: ";
    s << std::endl;
    Printer< ::geometry_msgs::Point_<ContainerAllocator> >::stream(s, indent + "  ", v.p_a);
    s << indent << "p_b: ";
    s << std::endl;
    Printer< ::geometry_msgs::Point_<ContainerAllocator> >::stream(s, indent + "  ", v.p_b);
    s << indent << "id: ";
    Printer<int32_t>::stream(s, indent + "  ", v.id);
  }
};

} // namespace message_operations
} // namespace ros

#endif // LASER_FEATURE_EXTRACTION_MESSAGE_LINEMSG_H
