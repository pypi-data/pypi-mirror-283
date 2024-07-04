"""KB json files test"""

import glob
import json
import pathlib

import pytest

CATEGORY_GROUPS = [
    "OWASP_MASVS_L1",
    "OWASP_MASVS_L2",
    "OWASP_MASVS_v2_1",
    "OWASP_MASVS_RESILIENCE",
    "CWE_TOP_25",
    "GDPR",
    "PCI_STANDARDS",
    "OWASP_ASVS_L1",
    "OWASP_ASVS_L2",
    "OWASP_ASVS_L3",
    "SOC2_CONTROLS",
]

OWASP_MASVS_L1 = [
    "MSTG_ARCH_1",
    "MSTG_ARCH_2",
    "MSTG_ARCH_3",
    "MSTG_ARCH_4",
    "MSTG_ARCH_12",
    "MSTG_STORAGE_1",
    "MSTG_STORAGE_2",
    "MSTG_STORAGE_3",
    "MSTG_STORAGE_4",
    "MSTG_STORAGE_5",
    "MSTG_STORAGE_6",
    "MSTG_STORAGE_7",
    "MSTG_STORAGE_12",
    "MSTG_CRYPTO_1",
    "MSTG_CRYPTO_2",
    "MSTG_CRYPTO_3",
    "MSTG_CRYPTO_4",
    "MSTG_CRYPTO_5",
    "MSTG_CRYPTO_6",
    "MSTG_AUTH_1",
    "MSTG_AUTH_2",
    "MSTG_AUTH_3",
    "MSTG_AUTH_4",
    "MSTG_AUTH_5",
    "MSTG_AUTH_6",
    "MSTG_AUTH_7",
    "MSTG_AUTH_12",
    "MSTG_NETWORK_1",
    "MSTG_NETWORK_2",
    "MSTG_NETWORK_3",
    "MSTG_PLATFORM_1",
    "MSTG_PLATFORM_2",
    "MSTG_PLATFORM_3",
    "MSTG_PLATFORM_4",
    "MSTG_PLATFORM_5",
    "MSTG_PLATFORM_6",
    "MSTG_PLATFORM_7",
    "MSTG_PLATFORM_8",
    "MSTG_CODE_1",
    "MSTG_CODE_2",
    "MSTG_CODE_3",
    "MSTG_CODE_4",
    "MSTG_CODE_5",
    "MSTG_CODE_6",
    "MSTG_CODE_7",
    "MSTG_CODE_8",
    "MSTG_CODE_9",
]

OWASP_MASVS_L2 = [
    "MSTG_ARCH_1",
    "MSTG_ARCH_2",
    "MSTG_ARCH_3",
    "MSTG_ARCH_4",
    "MSTG_ARCH_5",
    "MSTG_ARCH_6",
    "MSTG_ARCH_7",
    "MSTG_ARCH_8",
    "MSTG_ARCH_9",
    "MSTG_ARCH_10",
    "MSTG_ARCH_11",
    "MSTG_ARCH_12",
    "MSTG_STORAGE_1",
    "MSTG_STORAGE_2",
    "MSTG_STORAGE_3",
    "MSTG_STORAGE_4",
    "MSTG_STORAGE_5",
    "MSTG_STORAGE_6",
    "MSTG_STORAGE_7",
    "MSTG_STORAGE_8",
    "MSTG_STORAGE_9",
    "MSTG_STORAGE_10",
    "MSTG_STORAGE_11",
    "MSTG_STORAGE_12",
    "MSTG_STORAGE_13",
    "MSTG_STORAGE_14",
    "MSTG_STORAGE_15",
    "MSTG_CRYPTO_1",
    "MSTG_CRYPTO_2",
    "MSTG_CRYPTO_3",
    "MSTG_CRYPTO_4",
    "MSTG_CRYPTO_5",
    "MSTG_CRYPTO_6",
    "MSTG_AUTH_1",
    "MSTG_AUTH_2",
    "MSTG_AUTH_3",
    "MSTG_AUTH_4",
    "MSTG_AUTH_5",
    "MSTG_AUTH_6",
    "MSTG_AUTH_7",
    "MSTG_AUTH_8",
    "MSTG_AUTH_9",
    "MSTG_AUTH_10",
    "MSTG_AUTH_11",
    "MSTG_AUTH_12",
    "MSTG_NETWORK_1",
    "MSTG_NETWORK_2",
    "MSTG_NETWORK_3",
    "MSTG_NETWORK_4",
    "MSTG_NETWORK_5",
    "MSTG_NETWORK_6",
    "MSTG_PLATFORM_1",
    "MSTG_PLATFORM_2",
    "MSTG_PLATFORM_3",
    "MSTG_PLATFORM_4",
    "MSTG_PLATFORM_5",
    "MSTG_PLATFORM_6",
    "MSTG_PLATFORM_7",
    "MSTG_PLATFORM_8",
    "MSTG_PLATFORM_9",
    "MSTG_PLATFORM_10",
    "MSTG_PLATFORM_X",
    "MSTG_CODE_1",
    "MSTG_CODE_2",
    "MSTG_CODE_3",
    "MSTG_CODE_4",
    "MSTG_CODE_5",
    "MSTG_CODE_6",
    "MSTG_CODE_7",
    "MSTG_CODE_8",
    "MSTG_CODE_9",
]

OWASP_MASVS_v2_1 = [
    "MASVS_PRIVACY_1",
    "MASVS_PRIVACY_2",
    "MASVS_PRIVACY_3",
    "MASVS_PRIVACY_4",
    "MASVS_CODE_1",
    "MASVS_CODE_2",
    "MASVS_CODE_3",
    "MASVS_CODE_4",
    "MASVS_RESILIENCE_1",
    "MASVS_RESILIENCE_2",
    "MASVS_RESILIENCE_3",
    "MASVS_RESILIENCE_4",
    "MASVS_PLATFORM_1",
    "MASVS_PLATFORM_2",
    "MASVS_PLATFORM_3",
    "MASVS_NETWORK_1",
    "MASVS_NETWORK_2",
    "MASVS_AUTH_1",
    "MASVS_AUTH_2",
    "MASVS_AUTH_3",
    "MASVS_CRYPTO_1",
    "MASVS_CRYPTO_2",
    "MASVS_STORAGE_1",
    "MASVS_STORAGE_2",
]

OWASP_MASVS_RESILIENCE = [f"MSTG_RESILIENCE_{i}" for i in range(1, 13)]

CWE_TOP_25 = [
    "CWE_787",
    "CWE_79",
    "CWE_89",
    "CWE_20",
    "CWE_125",
    "CWE_78",
    "CWE_416",
    "CWE_22",
    "CWE_352",
    "CWE_434",
    "CWE_476",
    "CWE_502",
    "CWE_190",
    "CWE_287",
    "CWE_798",
    "CWE_862",
    "CWE_77",
    "CWE_306",
    "CWE_119",
    "CWE_276",
    "CWE_918",
    "CWE_362",
    "CWE_400",
    "CWE_611",
    "CWE_94",
]

GDPR = [f"ART_{i}" for i in range(1, 94)]

PCI_STANDARDS = [
    "REQ_1_1",
    "REQ_1_2",
    "REQ_1_3",
    "REQ_1_4",
    "REQ_1_5",
    "REQ_2_1",
    "REQ_2_2",
    "REQ_2_3",
    "REQ_3_1",
    "REQ_3_2",
    "REQ_3_3",
    "REQ_3_4",
    "REQ_3_5",
    "REQ_3_6",
    "REQ_3_7",
    "REQ_4_1",
    "REQ_4_2",
    "REQ_5_1",
    "REQ_5_2",
    "REQ_5_3",
    "REQ_5_4",
    "REQ_6_1",
    "REQ_6_2",
    "REQ_6_3",
    "REQ_6_4",
    "REQ_6_5",
    "REQ_7_1",
    "REQ_7_2",
    "REQ_7_3",
    "REQ_8_1",
    "REQ_8_2",
    "REQ_8_3",
    "REQ_8_4",
    "REQ_8_5",
    "REQ_8_6",
    "REQ_9_1",
    "REQ_9_2",
    "REQ_9_3",
    "REQ_9_4",
    "REQ_9_5",
    "REQ_10_1",
    "REQ_10_2",
    "REQ_10_3",
    "REQ_10_4",
    "REQ_10_5",
    "REQ_10_6",
    "REQ_10_7",
    "REQ_11_1",
    "REQ_11_2",
    "REQ_11_3",
    "REQ_11_4",
    "REQ_11_5",
    "REQ_11_6",
    "REQ_12_1",
    "REQ_12_2",
    "REQ_12_3",
    "REQ_12_4",
    "REQ_12_5",
    "REQ_12_6",
    "REQ_12_7",
    "REQ_12_8",
    "REQ_12_9",
    "REQ_12_10",
]

OWASP_ASVS_L1 = [
    "V2_1_1",
    "V2_1_2",
    "V2_1_3",
    "V2_1_4",
    "V2_1_5",
    "V2_1_6",
    "V2_1_7",
    "V2_1_8",
    "V2_1_9",
    "V2_1_10",
    "V2_1_11",
    "V2_1_12",
    "V2_2_1",
    "V2_2_2",
    "V2_2_3",
    "V2_3_1",
    "V2_5_1",
    "V2_5_2",
    "V2_5_3",
    "V2_5_4",
    "V2_5_5",
    "V2_5_6",
    "V2_7_1",
    "V2_7_2",
    "V2_7_3",
    "V2_7_4",
    "V2_8_1",
    "V3_1_1",
    "V3_2_1",
    "V3_2_2",
    "V3_2_3",
    "V3_3_1",
    "V3_3_2",
    "V3_4_1",
    "V3_4_2",
    "V3_4_3",
    "V3_4_4",
    "V3_4_5",
    "V3_7_1",
    "V4_1_1",
    "V4_1_2",
    "V4_1_3",
    "V4_1_5",
    "V4_2_1",
    "V4_2_2",
    "V4_3_1",
    "V4_3_2",
    "V5_1_1",
    "V5_1_2",
    "V5_1_3",
    "V5_1_4",
    "V5_1_5",
    "V5_2_1",
    "V5_2_2",
    "V5_2_3",
    "V5_2_4",
    "V5_2_5",
    "V5_2_6",
    "V5_2_7",
    "V5_2_8",
    "V5_3_1",
    "V5_3_2",
    "V5_3_3",
    "V5_3_4",
    "V5_3_5",
    "V5_3_6",
    "V5_3_7",
    "V5_3_8",
    "V5_3_9",
    "V5_3_10",
    "V5_5_1",
    "V5_5_2",
    "V5_5_3",
    "V5_5_4",
    "V6_2_1",
    "V7_1_1",
    "V7_1_2",
    "V7_4_1",
    "V8_2_1",
    "V8_2_2",
    "V8_2_3",
    "V8_3_1",
    "V8_3_2",
    "V8_3_3",
    "V8_3_4",
    "V9_1_1",
    "V9_1_2",
    "V9_1_3",
    "V10_3_1",
    "V10_3_2",
    "V10_3_3",
    "V11_1_1",
    "V11_1_2",
    "V11_1_3",
    "V11_1_4",
    "V11_1_5",
    "V12_1_1",
    "V12_3_1",
    "V12_3_2",
    "V12_3_3",
    "V12_3_4",
    "V12_3_5",
    "V12_4_1",
    "V12_4_2",
    "V12_5_1",
    "V12_5_2",
    "V12_6_1",
    "V13_1_1",
    "V13_1_3",
    "V13_2_1",
    "V13_2_2",
    "V13_2_3",
    "V13_3_1",
    "V14_2_1",
    "V14_2_2",
    "V14_2_3",
    "V14_3_2",
    "V14_3_3",
    "V14_4_1",
    "V14_4_2",
    "V14_4_3",
    "V14_4_4",
    "V14_4_5",
    "V14_4_6",
    "V14_4_7",
    "V14_5_1",
    "V14_5_2",
    "V14_5_3",
]

OWASP_ASVS_L2 = [
    "V1_1_1",
    "V1_1_2",
    "V1_1_3",
    "V1_1_4",
    "V1_1_5",
    "V1_1_6",
    "V1_1_7",
    "V1_2_1",
    "V1_2_2",
    "V1_2_3",
    "V1_2_4",
    "V1_4_1",
    "V1_4_4",
    "V1_4_5",
    "V1_5_1",
    "V1_5_2",
    "V1_5_3",
    "V1_5_4",
    "V1_6_1",
    "V1_6_2",
    "V1_6_3",
    "V1_6_4",
    "V1_7_1",
    "V1_7_2",
    "V1_8_1",
    "V1_8_2",
    "V1_9_1",
    "V1_9_2",
    "V1_10_1",
    "V1_11_1",
    "V1_11_2",
    "V1_12_2",
    "V1_14_1",
    "V1_14_2",
    "V1_14_3",
    "V1_14_4",
    "V1_14_5",
    "V1_14_6",
    "V2_1_1",
    "V2_1_2",
    "V2_1_3",
    "V2_1_4",
    "V2_1_5",
    "V2_1_6",
    "V2_1_7",
    "V2_1_8",
    "V2_1_9",
    "V2_1_10",
    "V2_1_11",
    "V2_1_12",
    "V2_2_1",
    "V2_2_2",
    "V2_2_3",
    "V2_3_1",
    "V2_3_2",
    "V2_3_3",
    "V2_4_1",
    "V2_4_2",
    "V2_4_3",
    "V2_4_4",
    "V2_4_5",
    "V2_5_1",
    "V2_5_2",
    "V2_5_3",
    "V2_5_4",
    "V2_5_5",
    "V2_5_6",
    "V2_5_7",
    "V2_6_1",
    "V2_6_2",
    "V2_6_3",
    "V2_7_1",
    "V2_7_2",
    "V2_7_3",
    "V2_7_4",
    "V2_7_5",
    "V2_7_6",
    "V2_8_1",
    "V2_8_2",
    "V2_8_3",
    "V2_8_4",
    "V2_8_5",
    "V2_8_6",
    "V2_8_7",
    "V2_9_1",
    "V2_9_2",
    "V2_9_3",
    "V2_10_1",
    "V2_10_2",
    "V2_10_3",
    "V2_10_4",
    "V3_1_1",
    "V3_2_1",
    "V3_2_2",
    "V3_2_3",
    "V3_2_4",
    "V3_3_1",
    "V3_3_2",
    "V3_3_3",
    "V3_3_4",
    "V3_4_1",
    "V3_4_2",
    "V3_4_3",
    "V3_4_4",
    "V3_4_5",
    "V3_5_1",
    "V3_5_2",
    "V3_5_3",
    "V3_7_1",
    "V4_1_1",
    "V4_1_2",
    "V4_1_3",
    "V4_1_5",
    "V4_2_1",
    "V4_2_2",
    "V4_3_1",
    "V4_3_2",
    "V4_3_3",
    "V5_1_1",
    "V5_1_2",
    "V5_1_3",
    "V5_1_4",
    "V5_1_5",
    "V5_2_1",
    "V5_2_2",
    "V5_2_3",
    "V5_2_4",
    "V5_2_5",
    "V5_2_6",
    "V5_2_7",
    "V5_2_8",
    "V5_3_1",
    "V5_3_2",
    "V5_3_3",
    "V5_3_4",
    "V5_3_5",
    "V5_3_6",
    "V5_3_7",
    "V5_3_8",
    "V5_3_9",
    "V5_3_10",
    "V5_4_1",
    "V5_4_2",
    "V5_4_3",
    "V5_5_1",
    "V5_5_2",
    "V5_5_3",
    "V5_5_4",
    "V6_1_1",
    "V6_1_2",
    "V6_1_3",
    "V6_2_1",
    "V6_2_2",
    "V6_2_3",
    "V6_2_4",
    "V6_2_5",
    "V6_2_6",
    "V6_3_1",
    "V6_3_2",
    "V6_4_1",
    "V6_4_2",
    "V7_1_1",
    "V7_1_2",
    "V7_1_3",
    "V7_1_4",
    "V7_2_1",
    "V7_2_2",
    "V7_3_1",
    "V7_3_3",
    "V7_3_4",
    "V7_4_1",
    "V7_4_2",
    "V7_4_3",
    "V8_1_1",
    "V8_1_2",
    "V8_1_3",
    "V8_1_4",
    "V8_2_1",
    "V8_2_2",
    "V8_2_3",
    "V8_3_1",
    "V8_3_2",
    "V8_3_3",
    "V8_3_4",
    "V8_3_5",
    "V8_3_6",
    "V8_3_7",
    "V8_3_8",
    "V9_1_1",
    "V9_1_2",
    "V9_1_3",
    "V9_2_1",
    "V9_2_2",
    "V9_2_3",
    "V9_2_4",
    "V10_2_1",
    "V10_2_2",
    "V10_3_1",
    "V10_3_2",
    "V10_3_3",
    "V11_1_1",
    "V11_1_2",
    "V11_1_3",
    "V11_1_4",
    "V11_1_5",
    "V11_1_6",
    "V11_1_7",
    "V11_1_8",
    "V12_1_1",
    "V12_1_2",
    "V12_1_3",
    "V12_2_1",
    "V12_3_1",
    "V12_3_2",
    "V12_3_3",
    "V12_3_4",
    "V12_3_5",
    "V12_3_6",
    "V12_4_1",
    "V12_4_2",
    "V12_5_1",
    "V12_5_2",
    "V12_6_1",
    "V13_1_1",
    "V13_1_3",
    "V13_1_4",
    "V13_1_5",
    "V13_2_1",
    "V13_2_2",
    "V13_2_3",
    "V13_2_5",
    "V13_2_6",
    "V13_3_1",
    "V13_3_2",
    "V13_4_1",
    "V13_4_2",
    "V14_1_1",
    "V14_1_2",
    "V14_1_3",
    "V14_1_4",
    "V14_2_1",
    "V14_2_2",
    "V14_2_3",
    "V14_2_4",
    "V14_2_5",
    "V14_2_6",
    "V14_3_2",
    "V14_3_3",
    "V14_4_1",
    "V14_4_2",
    "V14_4_3",
    "V14_4_4",
    "V14_4_5",
    "V14_4_6",
    "V14_4_7",
    "V14_5_1",
    "V14_5_2",
    "V14_5_3",
    "V14_5_4",
]

OWASP_ASVS_L3 = [
    "V1_1_1",
    "V1_1_2",
    "V1_1_3",
    "V1_1_4",
    "V1_1_5",
    "V1_1_6",
    "V1_1_7",
    "V1_2_1",
    "V1_2_2",
    "V1_2_3",
    "V1_2_4",
    "V1_4_1",
    "V1_4_2",
    "V1_4_3",
    "V1_4_4",
    "V1_4_5",
    "V1_5_1",
    "V1_5_2",
    "V1_5_3",
    "V1_5_4",
    "V1_6_1",
    "V1_6_2",
    "V1_6_3",
    "V1_6_4",
    "V1_7_1",
    "V1_7_2",
    "V1_8_1",
    "V1_8_2",
    "V1_9_1",
    "V1_9_2",
    "V1_10_1",
    "V1_11_1",
    "V1_11_2",
    "V1_11_3",
    "V1_12_1",
    "V1_12_2",
    "V1_14_1",
    "V1_14_2",
    "V1_14_3",
    "V1_14_4",
    "V1_14_5",
    "V1_14_6",
    "V2_1_1",
    "V2_1_2",
    "V2_1_3",
    "V2_1_4",
    "V2_1_5",
    "V2_1_6",
    "V2_1_7",
    "V2_1_8",
    "V2_1_9",
    "V2_1_10",
    "V2_1_11",
    "V2_1_12",
    "V2_2_1",
    "V2_2_2",
    "V2_2_3",
    "V2_2_4",
    "V2_2_5",
    "V2_2_6",
    "V2_2_7",
    "V2_3_1",
    "V2_3_2",
    "V2_3_3",
    "V2_4_1",
    "V2_4_2",
    "V2_4_3",
    "V2_4_4",
    "V2_4_5",
    "V2_5_1",
    "V2_5_2",
    "V2_5_3",
    "V2_5_4",
    "V2_5_5",
    "V2_5_6",
    "V2_5_7",
    "V2_6_1",
    "V2_6_2",
    "V2_6_3",
    "V2_7_1",
    "V2_7_2",
    "V2_7_3",
    "V2_7_4",
    "V2_7_5",
    "V2_7_6",
    "V2_8_1",
    "V2_8_2",
    "V2_8_3",
    "V2_8_4",
    "V2_8_5",
    "V2_8_6",
    "V2_8_7",
    "V2_9_1",
    "V2_9_2",
    "V2_9_3",
    "V2_10_1",
    "V2_10_2",
    "V2_10_3",
    "V2_10_4",
    "V3_1_1",
    "V3_2_1",
    "V3_2_2",
    "V3_2_3",
    "V3_2_4",
    "V3_3_1",
    "V3_3_2",
    "V3_3_3",
    "V3_3_4",
    "V3_4_1",
    "V3_4_2",
    "V3_4_3",
    "V3_4_4",
    "V3_4_5",
    "V3_5_1",
    "V3_5_2",
    "V3_5_3",
    "V3_6_1",
    "V3_6_2",
    "V3_7_1",
    "V4_1_1",
    "V4_1_2",
    "V4_1_3",
    "V4_1_4",
    "V4_1_5",
    "V4_2_1",
    "V4_2_2",
    "V4_3_1",
    "V4_3_2",
    "V4_3_3",
    "V5_1_1",
    "V5_1_2",
    "V5_1_3",
    "V5_1_4",
    "V5_1_5",
    "V5_2_1",
    "V5_2_2",
    "V5_2_3",
    "V5_2_4",
    "V5_2_5",
    "V5_2_6",
    "V5_2_7",
    "V5_2_8",
    "V5_3_1",
    "V5_3_2",
    "V5_3_3",
    "V5_3_4",
    "V5_3_5",
    "V5_3_6",
    "V5_3_7",
    "V5_3_8",
    "V5_3_9",
    "V5_3_10",
    "V5_4_1",
    "V5_4_2",
    "V5_4_3",
    "V5_5_1",
    "V5_5_2",
    "V5_5_3",
    "V5_5_4",
    "V6_1_1",
    "V6_1_2",
    "V6_1_3",
    "V6_2_1",
    "V6_2_2",
    "V6_2_3",
    "V6_2_4",
    "V6_2_5",
    "V6_2_6",
    "V6_2_7",
    "V6_2_8",
    "V6_3_1",
    "V6_3_2",
    "V6_3_3",
    "V6_4_1",
    "V6_4_2",
    "V7_1_1",
    "V7_1_2",
    "V7_1_3",
    "V7_1_4",
    "V7_2_1",
    "V7_2_2",
    "V7_3_1",
    "V7_3_2",
    "V7_3_3",
    "V7_3_4",
    "V7_4_1",
    "V7_4_2",
    "V7_4_3",
    "V8_1_1",
    "V8_1_2",
    "V8_1_3",
    "V8_1_4",
    "V8_1_5",
    "V8_1_6",
    "V8_2_1",
    "V8_2_2",
    "V8_2_3",
    "V8_3_1",
    "V8_3_2",
    "V8_3_3",
    "V8_3_4",
    "V8_3_5",
    "V8_3_6",
    "V8_3_7",
    "V8_3_8",
    "V9_1_1",
    "V9_1_2",
    "V9_1_3",
    "V9_2_1",
    "V9_2_2",
    "V9_2_3",
    "V9_2_4",
    "V9_2_5",
    "V10_1_1",
    "V10_2_1",
    "V10_2_2",
    "V10_2_3",
    "V10_2_4",
    "V10_2_5",
    "V10_2_6",
    "V10_3_1",
    "V10_3_2",
    "V10_3_3",
    "V11_1_1",
    "V11_1_2",
    "V11_1_3",
    "V11_1_4",
    "V11_1_5",
    "V11_1_6",
    "V11_1_7",
    "V11_1_8",
    "V12_1_1",
    "V12_1_2",
    "V12_1_3",
    "V12_2_1",
    "V12_3_1",
    "V12_3_2",
    "V12_3_3",
    "V12_3_4",
    "V12_3_5",
    "V12_3_6",
    "V12_4_1",
    "V12_4_2",
    "V12_5_1",
    "V12_5_2",
    "V12_6_1",
    "V13_1_1",
    "V13_1_2",
    "V13_1_3",
    "V13_1_4",
    "V13_1_5",
    "V13_2_1",
    "V13_2_2",
    "V13_2_3",
    "V13_2_4",
    "V13_2_5",
    "V13_2_6",
    "V13_3_1",
    "V13_3_2",
    "V13_4_1",
    "V13_4_2",
    "V14_1_1",
    "V14_1_2",
    "V14_1_3",
    "V14_1_4",
    "V14_1_5",
    "V14_2_1",
    "V14_2_2",
    "V14_2_3",
    "V14_2_4",
    "V14_2_5",
    "V14_2_6",
    "V14_3_1",
    "V14_3_2",
    "V14_3_3",
    "V14_4_1",
    "V14_4_2",
    "V14_4_3",
    "V14_4_4",
    "V14_4_5",
    "V14_4_6",
    "V14_4_7",
    "V14_5_1",
    "V14_5_2",
    "V14_5_3",
    "V14_5_4",
]

SOC2_CONTROLS = [
    "CC_1_1",
    "CC_1_2",
    "CC_1_3",
    "CC_1_4",
    "CC_1_5",
    "CC_2_1",
    "CC_2_2",
    "CC_2_3",
    "CC_3_1",
    "CC_3_2",
    "CC_3_3",
    "CC_3_4",
    "CC_4_1",
    "CC_4_2",
    "CC_5_1",
    "CC_5_2",
    "CC_5_3",
    "CC_6_1",
    "CC_6_2",
    "CC_6_3",
    "CC_6_4",
    "CC_6_5",
    "CC_6_6",
    "CC_6_7",
    "CC_6_8",
    "CC_7_1",
    "CC_7_2",
    "CC_7_3",
    "CC_7_4",
    "CC_7_5",
    "CC_8_1",
    "CC_9_1",
    "CC_9_2",
]


def testJsonFiles_allFilesAreValid_testPasses() -> None:
    path = pathlib.Path(__file__).parent.parent
    json_files = glob.glob(str(path) + "/**/*.json", recursive=True)

    for json_file in json_files:
        with pathlib.Path(json_file).open(encoding="utf-8") as file:
            try:
                json_data = json.load(file)
            except ValueError as e:
                pytest.fail(f"Failed to load JSON file '{json_file}': {str(e)}")

            # Check if the JSON data is a dictionary
            assert isinstance(json_data, dict), "JSON data must be a dictionary."

            # Check if the required keys are present
            required_keys = ["risk_rating", "short_description", "references", "title"]
            for key in required_keys:
                assert (
                    key in json_data
                ), f"Required key '{key}' is missing in JSON data."

            # Check the data types and formats of the keys
            assert isinstance(
                json_data["risk_rating"], str
            ), "risk_rating must be a string."
            assert isinstance(
                json_data["short_description"], str
            ), "short_description must be a string."
            assert isinstance(
                json_data["references"], dict
            ), "references must be a dictionary."
            assert isinstance(json_data["title"], str), "title must be a string."

            # Check the format of the references
            references = json_data["references"]
            assert isinstance(references, dict), "references must be a dictionary."


def testKbEntries_always_namesOfTheEntryFolderShouldAllBeUnique() -> None:
    """Ensure all the folders of the KB entries are unique across mobile & web (& potentially any new group)
    Example of the PATH_TRAVERSAL entry:
        MOBILE_CLIENT/ANDROID/_MEDIUM/PATH_TRAVERSAL/meta.json
        WEB_SERVICE/WEB/_HIGH/PATH_TRAVERSAL/meta.json
    """
    json_files = glob.glob("**/*.json", recursive=True)
    entry_names = [f.split("/")[3] for f in json_files]

    assert len(entry_names) == len(set(entry_names))
    assert "PATH_TRAVERSAL" in entry_names
    assert "XPATH_INJECTION" in entry_names
    assert "XML_INJECTION" in entry_names
    assert "WEB_PATH_TRAVERSAL" in entry_names
    assert "WEB_XPATH_INJECTION" in entry_names
    assert "WEB_XML_INJECTION" in entry_names


@pytest.mark.parametrize(
    "category, expected_categories",
    [
        ("OWASP_MASVS_L1", OWASP_MASVS_L1),
        ("OWASP_MASVS_L2", OWASP_MASVS_L2),
        ("OWASP_MASVS_v2_1", OWASP_MASVS_v2_1),
        ("OWASP_MASVS_RESILIENCE", OWASP_MASVS_RESILIENCE),
        ("CWE_TOP_25", CWE_TOP_25),
        ("GDPR", GDPR),
        ("PCI_STANDARDS", PCI_STANDARDS),
        ("OWASP_ASVS_L1", OWASP_ASVS_L1),
        ("OWASP_ASVS_L2", OWASP_ASVS_L2),
        ("OWASP_ASVS_L3", OWASP_ASVS_L3),
        ("SOC2_CONTROLS", SOC2_CONTROLS),
    ],
)
def testJsonFiles_allFilesHaveCorrectCategories_testPasses(
    category: str, expected_categories: list[str]
) -> None:
    """Test that all JSON files have the correct categories."""
    path = pathlib.Path(__file__).parent.parent
    json_files = glob.glob(str(path) + "/**/*.json", recursive=True)

    for json_file in json_files:
        with pathlib.Path(json_file).open(encoding="utf-8") as file:
            try:
                json_data = json.load(file)
            except ValueError as e:
                pytest.fail(f"Failed to load JSON file '{json_file}': {str(e)}")

            categories = json_data.get("categories", {})
            standard_categories = categories.get(category, [])

            for standard_category in standard_categories:
                assert standard_category in expected_categories


def testJsonFiles_whenFileHasCategories_shouldBeValid() -> None:
    """Test that all JSON files have the correct category groups."""
    path = pathlib.Path(__file__).parent.parent
    json_files = glob.glob(str(path) + "/**/*.json", recursive=True)

    for json_file in json_files:
        with pathlib.Path(json_file).open(encoding="utf-8") as file:
            try:
                json_data = json.load(file)
            except ValueError as e:
                pytest.fail(f"Failed to load JSON file '{json_file}': {str(e)}")

            categories = json_data.get("categories", {})

            assert (
                all(group_key in CATEGORY_GROUPS for group_key in categories.keys())
                is True
            )
