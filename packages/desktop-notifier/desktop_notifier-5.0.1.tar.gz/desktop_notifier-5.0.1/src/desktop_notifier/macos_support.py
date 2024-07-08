# -*- coding: utf-8 -*-
from __future__ import annotations

import platform
import ctypes

from typing import cast

from packaging.version import Version
from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library


macos_version = Version(platform.mac_ver()[0])


__all__ = [
    "is_bundle",
    "is_signed_bundle",
    "macos_version",
]


sec = load_library("Security")
foundation = load_library("Foundation")

NSBundle = ObjCClass("NSBundle")

# Security/SecRequirement.h

kSecCSDefaultFlags = 0
kSecCSCheckAllArchitectures = 1 << 0
kSecCSDoNotValidateExecutable = 1 << 1
kSecCSDoNotValidateResources = 1 << 2
kSecCSCheckNestedCode = 1 << 3
kSecCSStrictValidate = 1 << 4


def is_bundle() -> bool:
    """
    Detect if we are in an app bundle

    :returns: Whether we are inside an app bundle.
    """
    main_bundle = NSBundle.mainBundle
    return main_bundle.bundleIdentifier is not None


def is_signed_bundle() -> bool:
    """
    Detect if we are in a signed app bundle

    :returns: Whether we are inside a signed app bundle.
    """
    main_bundle = NSBundle.mainBundle

    if main_bundle.bundleIdentifier is None:
        return False

    # Check for valid signature.
    static_code = ctypes.c_void_p(0)
    err = sec.SecStaticCodeCreateWithPath(
        main_bundle.bundleURL, kSecCSDefaultFlags, ctypes.byref(static_code)
    )

    if err != 0:
        return False

    signed_status = sec.SecStaticCodeCheckValidity(
        static_code,
        kSecCSCheckAllArchitectures | kSecCSCheckNestedCode | kSecCSStrictValidate,
        None,
    )

    return cast(int, signed_status) == 0
