import zeep
import numpy as np

client = zeep.Client('http://turbulence.pha.jhu.edu/service/turbulence.asmx?WSDL')
ArrayOfFloat = client.get_type('ns0:ArrayOfFloat')
ArrayOfArrayOfFloat = client.get_type('ns0:ArrayOfArrayOfFloat')
SpatialInterpolation = client.get_type('ns0:SpatialInterpolation')
TemporalInterpolation = client.get_type('ns0:TemporalInterpolation')

token="edu.jhu.pha.turbulence.testing-201406" #replace with your own token

nnp=5 #number of points
points=np.random.rand(nnp,3)

# convert to JHTDB structures
x_coor=ArrayOfFloat(points[:,0].tolist())
y_coor=ArrayOfFloat(points[:,1].tolist())
z_coor=ArrayOfFloat(points[:,2].tolist())
point=ArrayOfArrayOfFloat([x_coor,y_coor,z_coor]);

print(points)

Function_name="GetVelocityGradient" 
time=0.6
number_of_component=9 # change this based on function_name, see http://turbulence.pha.jhu.edu/webquery/query.aspx

result=client.service.GetData_Python(Function_name, token,"isotropic1024coarse", 0.6, 
                                     SpatialInterpolation("None_Fd4"), TemporalInterpolation("None"), point)

print(result)