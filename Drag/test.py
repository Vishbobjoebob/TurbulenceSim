import zeep
import numpy as np
import math

client = zeep.Client('http://turbulence.pha.jhu.edu/service/turbulence.asmx?WSDL')
ArrayOfFloat = client.get_type('ns0:ArrayOfFloat')
ArrayOfPoint3 = client.get_type('ns0:ArrayOfPoint3')
Point3 = client.get_type('ns0:Point3')
Vector3 = client.get_type('ns0:Vector3')
ArrayOfArrayOfFloat = client.get_type('ns0:ArrayOfArrayOfFloat')
SpatialInterpolation = client.get_type('ns0:SpatialInterpolation')
TemporalInterpolation = client.get_type('ns0:TemporalInterpolation')

grid_size = 1000

token="com.gmail.pasamvishnu.reddy-e1b41e88" #replace with your own token

# nnp=5 #number of points
# x_range=[]
# y_range=[]
# points=[[[]]]
# for x in range(grid_size+1):
#     x_range.append((2*math.pi*x/1000))
# for y in range(grid_size+1):
#     y_range.append((2*math.pi*y/1000))

# for x in x_range:
#     for y in y_range:
#         points.append([x,y,0])

# print(points[4])

# # convert to JHTDB structures
# x_coor=ArrayOfFloat(points[:,0].tolist())
# y_coor=ArrayOfFloat(points[:,1].tolist())
# z_coor=ArrayOfFloat(points[:,2].tolist())
# point=ArrayOfArrayOfFloat([x_coor,y_coor,z_coor])
# Function_name="GetVelocity"
# number_of_component=3 # change this based on function_name, see http://turbulence.pha.jhu.edu/webquery/query.aspx

# result=client.service.GetVelocity(token,"isotropic1024coarse", 0.6,
#                                          SpatialInterpolation("None"),TemporalInterpolation("None"), point)
# print(result)

nnp=5 #number of points
points=np.random.rand(nnp,3)

# convert to JHTDB structures
x_coor=ArrayOfFloat(points[:,0].tolist())
y_coor=ArrayOfFloat(points[:,1].tolist())
z_coor=ArrayOfFloat(points[:,2].tolist())
point=ArrayOfPoint3([Point3(0.3,0.3,0), Point3(0.3,0.3,0),Point3(0.3,0.3,0)])

Function_name="GetVelocityHessian" 
time=0.6
number_of_component=3 # change this based on function_name, see http://turbulence.pha.jhu.edu/webquery/query.aspx

result=client.service.GetVelocity(token,"isotropic1024coarse", 0.6, 
                                     SpatialInterpolation("None"), TemporalInterpolation("None"), point)


print(result[0] + result[1])
