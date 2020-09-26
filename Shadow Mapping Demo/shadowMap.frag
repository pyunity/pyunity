#version 120                                                     
                                                                                    
void main()                                                                         
{
	float z = gl_FragCoord.z;
	float n = 1.0;
	float f = 1000.0;
	float c = (2.0 * n) / (f + n - z * (f - n));//linear conversion from www.roxlu.com/2014/036/rendering-the-depth-buffer                            
	gl_FragDepth = c;
}
