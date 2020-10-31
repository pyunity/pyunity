#version 120

uniform mat4 u_biasMVPMatrix;
varying vec4 v_shadowCoord;
varying vec3 v_position;
varying vec3 v_normal;
varying mat4 v_mvMatrix;

void main()
{
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
	v_position = vec3(gl_ModelViewMatrix * gl_Vertex);
	v_shadowCoord = u_biasMVPMatrix * gl_Vertex;
	v_mvMatrix = gl_ModelViewMatrix;
	v_normal = normalize(gl_NormalMatrix * gl_Normal);
	gl_TexCoord[0] = gl_MultiTexCoord0;
}
