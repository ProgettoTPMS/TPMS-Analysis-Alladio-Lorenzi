#include <cmath>
#include "Utils.h"

using namespace std;


// Implementation of the function defined in Utils.h

void TpmsSolidGenerator(const int npoints, const int numcellx, const int numcelly, const int numcellz, char type, const float rvalue, vtkImageData* volume, const float scaleVtk)
{
	// int dimx = npoints * numcellx + 2*(int)scaleVtk + 1;
	// int dimy = npoints * numcelly + 2*(int)scaleVtk + 1;
	// int dimz = npoints * numcellz + 2*(int)scaleVtk + 1;
	int dimx = npoints * numcellx + 2;
	int dimy = npoints * numcelly + 2;
	int dimz = npoints * numcellz + 2;
	int dimension = max({dimx, dimy, dimz});

	const float pi2 = 2 * 3.14159265358979323846 / npoints;
	float scal = 0.;

	float* cosv = new float[dimension];
	for (int i = 0; i < dimension; i++)
		cosv[i] = cos(pi2 * i);

	float* senv = new float[dimension];
	for (int i = 0; i < dimension; i++)
		senv[i] = sin(pi2 * i);

	float* cosv_t = new float[dimension];
	if ((type == 'I') || (type == 'S') || (type == 'F')|(type == 'L'))
		for (int i = 0; i < dimension; i++)
			cosv_t[i] = cos(2 * pi2 * i);
	float* senv_t = new float[dimension];
	if ((type == 'I') || (type == 'S') || (type == 'F')||(type == 'L'))
		for (int i = 0; i < dimension; i++)
			senv_t[i] = sin(2 * pi2 * i);

	int temp = 0;

	switch (type)
	{

		// SCHWARZ_PRIMITIVE
	case 'P': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = (cosv[x] + cosv[y] + cosv[z]) - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;


		// SHOEN_GYROID
	case 'G': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = cosv[x] * senv[y] + cosv[y] * senv[z] + cosv[z] * senv[x] - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;


		// SCHWARZ_DIAMOND
	case 'D': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = senv[x] * senv[y] * senv[z] + senv[x] * cosv[y] * cosv[z] + cosv[x] * senv[y] * cosv[z] + cosv[x] * cosv[y] * senv[z] - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;


		// SHOEN_IWP
	case 'I': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = 2. * (cosv[x] * cosv[y] + cosv[y] * cosv[z] + cosv[z] * cosv[x]) - (cosv_t[x] + cosv_t[y] + cosv_t[z]) - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;


		// FISCHER_KOCH_S
	case 'S': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = cosv_t[x] * senv[y] * cosv[z] + cosv[x] * cosv_t[y] * senv[z] + senv[x] * cosv[y] * cosv_t[z] - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;


		// F_RD
	case 'F': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = -(4. * (cosv[x] * cosv[y] * cosv[z]) - (cosv_t[x] * cosv_t[y] + cosv_t[y] * cosv_t[z] + cosv_t[z] * cosv_t[x])) - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;

	

		// Split P1
	case 'L': {
		for (int z = 0; z < dimz; z++)
			for (int y = 0; y < dimy; y++)
				for (int x = 0; x < dimx; x++) {
					scal = (1.1*(senv_t[x]*senv[z]*cosv[y]+senv_t[y]*senv[x]*cosv[z]+senv_t[z]*senv[y]*cosv[x])-0.2*(cosv_t[x]*cosv_t[y]+cosv_t[y]*cosv_t[z]+cosv_t[z]*cosv_t[x])-0.4*(cosv_t[x]*cosv_t[y]*cosv_t[z])) - rvalue;
					float* a = static_cast<float*> (volume->GetScalarPointer(x, y, z));
					*a = scal;
					temp++;
				}
	} break;
	}	

	delete[] cosv;
	delete[] senv;
	delete[] cosv_t;
	delete[] senv_t;

	

}
