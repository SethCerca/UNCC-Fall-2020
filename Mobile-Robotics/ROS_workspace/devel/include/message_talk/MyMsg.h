// Generated by gencpp from file message_talk/MyMsg.msg
// DO NOT EDIT!


#ifndef MESSAGE_TALK_MESSAGE_MYMSG_H
#define MESSAGE_TALK_MESSAGE_MYMSG_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace message_talk
{
template <class ContainerAllocator>
struct MyMsg_
{
  typedef MyMsg_<ContainerAllocator> Type;

  MyMsg_()
    : id(0)
    , message()  {
    }
  MyMsg_(const ContainerAllocator& _alloc)
    : id(0)
    , message(_alloc)  {
  (void)_alloc;
    }



   typedef uint32_t _id_type;
  _id_type id;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _message_type;
  _message_type message;





  typedef boost::shared_ptr< ::message_talk::MyMsg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::message_talk::MyMsg_<ContainerAllocator> const> ConstPtr;

}; // struct MyMsg_

typedef ::message_talk::MyMsg_<std::allocator<void> > MyMsg;

typedef boost::shared_ptr< ::message_talk::MyMsg > MyMsgPtr;
typedef boost::shared_ptr< ::message_talk::MyMsg const> MyMsgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::message_talk::MyMsg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::message_talk::MyMsg_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace message_talk

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'message_talk': ['/home/turtlebot/ros_workspace/src/message_talk/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::message_talk::MyMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::message_talk::MyMsg_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::message_talk::MyMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::message_talk::MyMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::message_talk::MyMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::message_talk::MyMsg_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::message_talk::MyMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a0fde650e5c7c5d45c12525040ddb219";
  }

  static const char* value(const ::message_talk::MyMsg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa0fde650e5c7c5d4ULL;
  static const uint64_t static_value2 = 0x5c12525040ddb219ULL;
};

template<class ContainerAllocator>
struct DataType< ::message_talk::MyMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "message_talk/MyMsg";
  }

  static const char* value(const ::message_talk::MyMsg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::message_talk::MyMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint32 id\n\
string message\n\
";
  }

  static const char* value(const ::message_talk::MyMsg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::message_talk::MyMsg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.message);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MyMsg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::message_talk::MyMsg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::message_talk::MyMsg_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.id);
    s << indent << "message: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.message);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MESSAGE_TALK_MESSAGE_MYMSG_H
