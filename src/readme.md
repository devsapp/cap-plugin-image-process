
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# image-process-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=image-process-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=image-process-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=image-process-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=image-process-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=image-process-v3&type=packageDownload">
  </a>
</p>

<description>

本案例将 Wand，这一功能强大、易于使用的Python图像处理库，快速搭建并部署到阿里云函数计算 FC。

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/image-process/tree/V3/src)

</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=image-process-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=image-process-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init image-process-v3 -d image-process-v3`
  - 进入项目，并进行项目部署：`cd image-process-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

本案例将 Wand，这一功能强大、易于使用的Python图像处理库，快速搭建并部署到阿里云函数计算 FC。

Wand 提供了一个简单的API来创建、读取、保存、编辑和显示图像。这个库在执行复杂的图像操作时能够保持较高的性能，并且在Windows、Linux、macOS和其他支持Python的平台上都能运行。Wand支持多种常见的图像文件格式，包括JPEG、PNG、GIF等，并提供了便捷的方法来读取和保存这些格式的文件。

Wand的图像处理功能丰富，包括修剪、缩放、旋转、合并等基本操作，以及滤镜、调整亮度、对比度等高级功能。这使得开发者能够轻松实现各种图像处理需求。

通过 Serverless 开发平台，您只需要几步，就可以体验 wand 图片处理库 ，并享受 Serverless 架构带来的降本提效的技术红利。

</appdetail>

## 使用流程

<usedetail id="flushContent">

### 查看部署的案例

部署完成之后，您可以看到系统返回给您的案例地址，点开url，就可以看到图片处理首页：

![](https://img.alicdn.com/imgextra/i1/O1CN019J0wHL1i0LpODWgIf_!!6000000004350-0-tps-2868-1554.jpg)

在对象存储oss中上传存储图片，从oss中获取目标图片，如：rockuw-sh/图片名

根据不同的请求路径，使用python [wand](https://docs.wand-py.org/en/0.5.6/index.html)图片处理库进行常见的图片处理：

| 功能   | 请求路径      | 参数                                                    |   
|------|-----------|-------------------------------------------------------|  
| 拼接   | /pinjie   | left=bucket/image1.jpg&right=bucket/image2.jpg        |    
| 水印   | /watermark | img=bucket/image.jpg&text=hello-fc                    |    
| 格式转换 | /format   | img=bucket/image.jpg&fmt=png                          |    
| 图片转灰 | /gray | img=bucket/image.jpg(or .png,jpeg,webp)               |
| 保存结果 | 上述参数均可    | img=bucket/image.jpg&fmt=png&target=bucket/output.png |

### 二次开发

您可以通过云端控制台的开发功能进行二次开发。如果您之前是在本地创建的项目案例，也可以在本地项目目录`image-process-v3`文件夹下，对项目进行二次开发。开发完成后，可以通过`s deploy`进行快速部署。


</usedetail>

## 注意事项

<matters id="flushContent">
</matters>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
