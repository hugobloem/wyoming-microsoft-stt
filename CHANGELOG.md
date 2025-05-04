# Changelog

## [1.3.1](https://github.com/hugobloem/wyoming-microsoft-stt/compare/v1.3.0...v1.3.1) (2025-05-04)


### 🐛 Bugfixes

* stop stream when last chunk is sent ([#79](https://github.com/hugobloem/wyoming-microsoft-stt/issues/79)) ([4eba565](https://github.com/hugobloem/wyoming-microsoft-stt/commit/4eba5650fa92bb9cc3e7448617412cd82ed861b4))

## [1.3.0](https://github.com/hugobloem/wyoming-microsoft-stt/compare/v1.2.1...v1.3.0) (2025-05-03)


### 🚀 Features

* Add multilingual support for transcription ([#77](https://github.com/hugobloem/wyoming-microsoft-stt/issues/77)) ([e4d25cb](https://github.com/hugobloem/wyoming-microsoft-stt/commit/e4d25cb8223852faff476a540db9709a654b31c1))
* Use real-time STT [@nuzayets](https://github.com/nuzayets) ([8f5c0f2](https://github.com/hugobloem/wyoming-microsoft-stt/commit/8f5c0f2c37e97e13ba9fe190a6ada86a6acff4cd))


### 🔧 Miscellaneous Chores

* bump azure-cognitiveservices-speech from 1.42.0 to 1.43.0 ([#74](https://github.com/hugobloem/wyoming-microsoft-stt/issues/74)) ([29c9c00](https://github.com/hugobloem/wyoming-microsoft-stt/commit/29c9c00af63e65dc467a796de4d570905cf74184))


### 👷 Continuous Integration

* reduce python versions in test ([#75](https://github.com/hugobloem/wyoming-microsoft-stt/issues/75)) ([036c83a](https://github.com/hugobloem/wyoming-microsoft-stt/commit/036c83a6515bb075a606183b3e0922b463ee0d1e))
* run release please on-demand ([#78](https://github.com/hugobloem/wyoming-microsoft-stt/issues/78)) ([d5094f5](https://github.com/hugobloem/wyoming-microsoft-stt/commit/d5094f58b6996087b448f854225b48c0bd3abecc))

## [1.2.1](https://github.com/hugobloem/wyoming-microsoft-stt/compare/v1.2.0...v1.2.1) (2025-02-23)


### 🐛 Bugfixes

* profanity filter should be `off` not `raw` ([#71](https://github.com/hugobloem/wyoming-microsoft-stt/issues/71)) ([8727b1f](https://github.com/hugobloem/wyoming-microsoft-stt/commit/8727b1fa06a58d239a341c59be3f8db5a101c8c9))

## [1.2.0](https://github.com/hugobloem/wyoming-microsoft-stt/compare/v1.1.0...v1.2.0) (2025-02-23)


### 🚀 Features

* add profanity filter ([35a8a25](https://github.com/hugobloem/wyoming-microsoft-stt/commit/35a8a251751bf8d0828c3ec9af74ef5dbb621f18))


### 🔨 Code Refactoring

* use Pydantic model for Microsoft STT configuration ([35a8a25](https://github.com/hugobloem/wyoming-microsoft-stt/commit/35a8a251751bf8d0828c3ec9af74ef5dbb621f18))

## [1.1.0](https://github.com/hugobloem/wyoming-microsoft-stt/compare/1.0.7...v1.1.0) (2024-11-20)


### 🚀 Features

* Added env variables for secrets, additional logging, and consistent writing to /tmp ([#63](https://github.com/hugobloem/wyoming-microsoft-stt/issues/63)) ([1ae559d](https://github.com/hugobloem/wyoming-microsoft-stt/commit/1ae559dc4f2d0d29c51f01a281eb38d1c32df9e1))


### 🐛 Bugfixes

* enable release-please for the `main` branch ([47baf85](https://github.com/hugobloem/wyoming-microsoft-stt/commit/47baf851af3789f218f024b527bdf52cc9b039e5))


### 🔨 Code Refactoring

* update MicrosoftSTT fixture to return arguments instead of instance ([#64](https://github.com/hugobloem/wyoming-microsoft-stt/issues/64)) ([299b3fe](https://github.com/hugobloem/wyoming-microsoft-stt/commit/299b3fec41d320a154624b3d9928c4cc4fd68e54))


### 🎨 Styles

* Rename release_please.yaml to release-please.yaml ([baf2120](https://github.com/hugobloem/wyoming-microsoft-stt/commit/baf21200dac953bd6535bd34dbfe6c853af40a59))


### 👷 Continuous Integration

* Add release-please configuration and workflow files ([#65](https://github.com/hugobloem/wyoming-microsoft-stt/issues/65)) ([8b03951](https://github.com/hugobloem/wyoming-microsoft-stt/commit/8b03951732461a7f3ad032c5820a5ec1f48e8e41))
