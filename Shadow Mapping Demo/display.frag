#version 120                                                     

struct Light
{
    vec3 color;
    vec3 direction;
    vec3 position;
    float innerAngle;
    float outerAngle;
};

uniform sampler2D u_modelTexture;
uniform sampler2D u_shadowMap;
varying vec4 v_shadowCoord;
varying vec3 v_position;
varying vec3 v_normal;
varying mat4 v_mvMatrix;
uniform Light u_light;//spotlight in the demo!

vec4 calcShadow()
{
	vec3 projCoords = v_shadowCoord.xyz/v_shadowCoord.w;
	float closestDepth = texture2D(u_shadowMap, projCoords.xy).z;
	float z = projCoords.z;
	float n = 1.0;
	float f = 1000.0;
	float currentDepth = (2.0 * n) / (f + n - z * (f - n));
	vec3 shadow = u_light.color;
	float bias = 0.00005;//simple bias works here well enough, but needs to be tweaked based on the scene to avoid peter-panning.
	
	if(closestDepth + bias < currentDepth)
	{
		shadow = vec3(0.5, 0.5, 0.5);//ambient light
	}
	
	//We have artifacts on sides that should be in shadow. 
	//Let's remove those with a partial lighting calculation.
	vec3 normal = normalize(v_normal);
	vec3 lightPos = vec3(v_mvMatrix * vec4(u_light.position, 1.0));
	vec3 lightDir = normalize(lightPos - v_position);
	float diffCont = max(0.0, dot(normal, lightDir));
	if (diffCont == 0.0)
	{
		shadow = vec3(0.5, 0.5, 0.5);//ambient light
	}
	return vec4(shadow, 1.0);
}

vec3 calcLight()
{
	vec3 normal = normalize(v_normal);
	vec3 outLight = vec3(0.0, 0.0, 0.0);
	vec3 lightPos = vec3(v_mvMatrix * vec4(u_light.position, 1.0));
	vec3 spotDir = normalize(vec3(v_mvMatrix * vec4(u_light.direction, 0.0)));
	float innerAngle = u_light.innerAngle;
	float outerAngle = u_light.outerAngle;
	vec3 lightDiffuse = u_light.color;
	vec3 lightDir = normalize(lightPos - v_position);
	float diffCont = max(0.0, dot(normal, lightDir));
	if (diffCont > 0.0)
	{
		float angle = degrees(acos(dot(-lightDir, spotDir)));
		if (angle < outerAngle)
		{
			if (angle < innerAngle)
			{
				vec3 diffuse = diffCont * lightDiffuse;
				outLight = diffuse;
			}
			
			else
			{
				float att = 1 - pow(((angle - innerAngle) / (outerAngle - innerAngle)), 2);//squaring to approximate inverse-square law falloff
				vec3 diffuse = diffCont * lightDiffuse * att;
				outLight = diffuse;
			}
		}
	}
	return outLight;
}
															
void main()                                                                         
{
	vec3 ambientLight = vec3(0.5, 0.5, 0.5);
	vec3 diffuseLight = calcLight();
	vec4 totalLight = vec4(ambientLight + diffuseLight, 1.0);
	vec4 shadow = calcShadow();
	vec4 color = texture2D(u_modelTexture, gl_TexCoord[0].st);
	gl_FragColor = shadow * color * totalLight;
}
