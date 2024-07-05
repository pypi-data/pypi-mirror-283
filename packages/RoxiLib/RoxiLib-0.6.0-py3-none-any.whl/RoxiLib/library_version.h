/*
 * library_version.h
 *
 *  Created on: 16. 12. 2020
 *      Author: franekt
 */

#ifndef SOURCEDLL_LIBRARY_VERSION_H_
#define SOURCEDLL_LIBRARY_VERSION_H_

#include <stdint.h>
#include "roxi_api_common.h"
/**
 * @brief It returns version of library API
 *
 * @return Version is in format:
 *         | 1 B | 1 B |   1 B  | 1 B |
 *         |major|minor|revision|build|
 */

API_FUNC_PREFIX uint32_t rapi_get_library_version();

typedef struct rapi_lib_version_t {
    uint8_t major;
    uint8_t minor;
    uint8_t revision;
    uint8_t build;
}rapi_lib_version;

rapi_lib_version rapi_get_library_version_object(void);

#endif /* SOURCEDLL_LIBRARY_VERSION_H_ */
