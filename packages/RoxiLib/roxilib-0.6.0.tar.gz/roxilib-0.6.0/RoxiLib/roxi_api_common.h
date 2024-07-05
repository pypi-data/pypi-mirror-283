/*
 * roxi_api_common.h
 *
 *  Created on: 18. 1. 2023
 *      Author: Kučera Stanislav
 */

#ifndef SOURCEDLL_ROXI_API_COMMON_H_
#define SOURCEDLL_ROXI_API_COMMON_H_

#include <stdint.h>

#if _WIN32
#	define TYPEDEF_FUNC_PREFIX	__stdcall
#	define API_FUNC_PREFIX		__declspec(dllexport)
#endif /*_WIN32*/

#if __linux__
#	define TYPEDEF_FUNC_PREFIX	/*No Prefix*/
#	define API_FUNC_PREFIX		__attribute__((visibility ("default")))
#endif /*__linux__*/


#endif /* SOURCEDLL_ROXI_API_COMMON_H_ */
