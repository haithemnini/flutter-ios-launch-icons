# LaunchScreen.storyboard template

Replace brand hex / multipliers as needed. Image files must be loose bundle PNGs named `BrandLogo` / `BrandLogoNight`.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="com.apple.InterfaceBuilder3.CocoaTouch.Storyboard.XIB" version="3.0" toolsVersion="21701" targetRuntime="iOS.CocoaTouch" propertyAccessControl="none" useAutolayout="YES" launchScreen="YES" useTraitCollections="YES" colorMatched="YES" initialViewController="01J-lp-oVM">
    <device id="retina6_1" orientation="portrait" appearance="light"/>
    <dependencies>
        <deployment identifier="iOS"/>
        <plugIn identifier="com.apple.InterfaceBuilder.IBCocoaTouchPlugin" version="21678"/>
        <capability name="documents saved in the Xcode 8 format" minToolsVersion="8.0"/>
    </dependencies>
    <scenes>
        <scene sceneID="EHf-IW-A2E">
            <objects>
                <viewController id="01J-lp-oVM" sceneMemberID="viewController">
                    <view key="view" contentMode="scaleToFill" id="Ze5-6b-2t3">
                        <rect key="frame" x="0.0" y="0.0" width="414" height="896"/>
                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
                        <subviews>
                            <imageView clipsSubviews="YES" userInteractionEnabled="NO" contentMode="scaleAspectFit" image="BrandLogo" translatesAutoresizingMaskIntoConstraints="NO" id="brand-logo-view">
                                <rect key="frame" x="141" y="388" width="132" height="120"/>
                                <variation key="userInterfaceStyle=dark" image="BrandLogoNight"/>
                            </imageView>
                        </subviews>
                        <!-- Light ivory #FFFCF7 -->
                        <color key="backgroundColor" red="1" green="0.988235294117647" blue="0.968627450980392" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>
                        <variation key="userInterfaceStyle=dark">
                            <!-- Dark #17120E -->
                            <color key="backgroundColor" red="0.09019607843137255" green="0.07058823529411765" blue="0.054901960784313725" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>
                        </variation>
                        <constraints>
                            <constraint firstItem="brand-logo-view" firstAttribute="centerX" secondItem="Ze5-6b-2t3" secondAttribute="centerX" id="cX"/>
                            <constraint firstItem="brand-logo-view" firstAttribute="centerY" secondItem="Ze5-6b-2t3" secondAttribute="centerY" id="cY"/>
                            <constraint firstItem="brand-logo-view" firstAttribute="width" secondItem="Ze5-6b-2t3" secondAttribute="width" multiplier="0.32" id="w"/>
                            <constraint firstItem="brand-logo-view" firstAttribute="height" secondItem="brand-logo-view" secondAttribute="width" multiplier="0.9075" id="aspect"/>
                        </constraints>
                    </view>
                </viewController>
                <placeholder placeholderIdentifier="IBFirstResponder" id="iYj-Kq-Ea1" userLabel="First Responder" sceneMemberID="firstResponder"/>
            </objects>
            <point key="canvasLocation" x="53" y="375"/>
        </scene>
    </scenes>
    <resources>
        <image name="BrandLogo" width="400" height="363"/>
        <image name="BrandLogoNight" width="400" height="363"/>
    </resources>
</document>
```

## Trait keys that fail

| Key | Result |
|-----|--------|
| `userInterfaceStyle=dark` | Works; embeds night image |
| `interfaceStyle` | Compiles; does not switch image reliably |
| `luminosity=dark` / `appearance=dark` | Often crash `ibtool` |

## Aspect multiplier

`height = width * (logoHeight / logoWidth)`. For 400×363 use `0.9075`.
