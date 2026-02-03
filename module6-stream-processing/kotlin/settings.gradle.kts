pluginManagement {
    val kotlinVersion: String by settings
    val kaptVersion: String by settings
    val graalvmBuildToolsVersion: String by settings
    val shadowJarVersion: String by settings
    val detektVersion: String by settings

    plugins {
        kotlin("jvm") version kotlinVersion
        kotlin("kapt") version kaptVersion
        id("org.graalvm.buildtools.native") version graalvmBuildToolsVersion
        id("com.gradleup.shadow") version shadowJarVersion
        id("io.gitlab.arturbosch.detekt") version detektVersion
    }

    repositories {
        maven {
            url = uri("https://raw.githubusercontent.com/graalvm/native-build-tools/snapshots")
        }
        gradlePluginPortal()
    }
}

rootProject.name = "kotlin-sp"
