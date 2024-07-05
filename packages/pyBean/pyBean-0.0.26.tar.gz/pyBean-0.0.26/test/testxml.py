import xml.etree.ElementTree as ET

tree = ET.parse('resource/applicationContext.xml')
root = tree.getroot()

for bean in root.findall('{http://www.springframework.org/schema/beans}bean'):
    bean_id = bean.get('id')
    bean_class = bean.get('class')
    print(f"Bean ID: {bean_id}, Class: {bean_class}")

    for constructor_arg in bean.findall('{http://www.springframework.org/schema/beans}constructor-arg'):
        constructor_arg_value = constructor_arg.get('value')
        print(f"  Constructor Arg Value: {constructor_arg_value}")

    for property_element in bean.findall('{http://www.springframework.org/schema/beans}property'):
        property_name = property_element.get('name')
        property_value = property_element.get('value')
        property_ref = property_element.get('ref')
        print(f"  Property Name: {property_name}, Value: {property_value}, Ref: {property_ref}")
