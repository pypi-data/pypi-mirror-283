from pathlib import PurePath, Path
from tests.integration_tests.validation.conformance_suite_config import ConformanceSuiteConfig, ConformanceSuiteAssetConfig

config = ConformanceSuiteConfig(
    assets=[
        ConformanceSuiteAssetConfig.conformance_suite(
            Path("report-package-conformance.zip"),
            entry_point=Path("report-package-conformance/index.csv"),
        ),
    ],
    expected_failure_ids=frozenset(f"report-package-conformance/index.csv:{s}" for s in [
        "V-000-invalid-zip",
        "V-003-multiple-top-level-directories",
        "V-004-empty-zip",
        "V-005-leading-slash-in-zip-entry",
        "V-006-dot-slash-in-zip-entry",
        "V-007-dot-dot-slash-in-zip-entry",
        "V-008-double-slash-in-zip-entry",
        "V-009-backslash-in-zip-entry",
        "V-010-duplicate-paths-in-zip-entry",
        "V-011-duplicate-paths-in-zip-entry-dir-under-file",
        "V-012-encrypted-zip",
        "V-100-invalid-documentType",
        "V-101-missing-documentType",
        "V-102-invalid-documentInfo",
        "V-103-missing-documentInfo",
        "V-104-invalid-reportPackage-json",
        "V-105-invalid-reportPackage-json-duplicate-keys",
        "V-106-utf16-reportPackage-json",
        "V-107-utf7-reportPackage-json",
        "V-108-utf32-reportPackage-json",
        "V-200-unsupportedReportPackageVersion",
        "V-201-missing-report-package-json",
        "V-202-missing-report-package-json",
        "V-203-xbri-documentType",
        "V-204-xbr-documentType",
        "V-205-unconstrained-documentType",
        "V-206-xbri-documentType",
        "V-207-xbri-without-reportPackage-json",
        "V-208-xbri-without-reportPackage-json-and-reports",
        "V-209-xbr-without-reportPackage-json",
        "V-210-xbr-without-reportPackage-json-and-reports",
        "V-211-unsupported-file-extension",
        "V-300-xbri-with-single-xhtml",
        "V-301-xbri-with-single-ixds",
        "V-302-xbri-with-single-html",
        "V-303-xbri-with-single-htm",
        "V-304-xbri-with-no-taxonomy",
        "V-305-xbri-with-xhtml-in-dot-json-directory",
        "V-306-xbri-with-xhtml-in-dot-xbrl-directory",
        "V-400-xbri-without-reports-directory",
        "V-401-xbri-with-only-txt-in-reports-directory",
        "V-402-xbri-with-xhtml-too-deep",
        "V-403-xbri-with-multiple-reports",
        "V-404-xbri-with-json-report",
        "V-405-xbri-with-xbrl-report",
        "V-406-xbri-with-multiple-reports-in-a-subdirectory",
        "V-502-xbr-with-single-json",
        "V-503-xbr-with-single-csv",
        "V-504-xbr-with-single-xbrl",
        "V-505-xbr-with-single-xbrl-in-subdir",
        "V-506-xbr-with-single-json-and-extra-files",
        "V-507-xbr-with-single-json-with-bom",
        "V-508-xbr-with-no-taxonomy",
        "V-509-xbr-with-json-in-dot-xhtml-directory",
        "V-600-xbr-without-reports-directory",
        "V-601-xbr-with-only-txt-in-reports-directory",
        "V-603-xbr-with-invalid-jrr",
        "V-604-xbr-with-invalid-jrr-duplicate-keys",
        "V-605-xbr-with-invalid-jrr-utf32",
        "V-606-xbr-with-invalid-jrr-utf16",
        "V-607-xbr-with-invalid-jrr-utf7",
        "V-608-xbr-with-invalid-jrr-missing-documentInfo",
        "V-609-xbr-with-invalid-jrr-missing-documentType",
        "V-610-xbr-with-invalid-jrr-non-string-documentType",
        "V-611-xbr-with-invalid-jrr-non-object-documentInfo",
        "V-612-xbr-with-multiple-reports",
        "V-613-xbr-with-json-and-xbrl-too-deep",
        "V-614-xbr-with-xhtml-report",
        "V-615-xbr-with-html-report",
        "V-616-xbr-with-htm-report",
        "V-617-xbr-with-multiple-reports-in-a-subdirectory",
        "V-701-zip-with-no-taxonomy",
        "V-800-zip-without-reports-directory",
        "V-801-zip-with-only-txt-in-reports-directory",
        "V-802-zip-with-reports-too-deep",
        "V-803-zip-with-multiple-reports-in-a-subdirectory",
        "V-804-zip-with-multiple-reports-in-a-subdirectory-uppercase",
        "V-900-future-zip",
        "V-901-future-xbri",
        "V-902-future-xbr",
        "V-903-future-xbrx",
        "V-904-future-package-with-invalid-reportPackage-json",
        "V-905-future-package-with-invalid-reportPackage-json-duplicate-keys",
        "V-906-future-package-with-invalid-reportPackage-json-utf32",
        "V-907-future-package-with-invalid-reportPackage-json-utf16",
        "V-908-future-package-with-invalid-reportPackage-json-utf7",
        "V-909-future-package-with-invalid-reportPackage-json-missing-documentInfo",
        "V-910-future-package-with-invalid-reportPackage-json-missing-documentType",
        "V-911-future-package-with-invalid-reportPackage-json-non-string-documentType",
        "V-912-future-package-with-invalid-reportPackage-json-non-object-documentInfo",
        "V-913-future-package-with-bom-in-reportPackage-json",
        "V-914-current-and-future-package",
    ]),
    info_url="https://specifications.xbrl.org/work-product-index-taxonomy-packages-report-packages-1.0.html",
    membership_url="https://www.xbrl.org/join",
    name=PurePath(__file__).stem,
    network_or_cache_required=False,
)
