# WorldCopier

[![](https://img.shields.io/badge/for-mcdr2-9cf?style=for-the-badge&labelColor=blue)](https://github.com/Fallen-Breath/MCDReforged)

将镜像服与生存服同步。

> ⚠️ 仅支持同步整个存档，需要部分同步请用 [RegionFileUpdater](https://github.com/TISUnion/RegionFileUpdater)

## ❤️ 特别感谢

这个插件的大部分代码来自 [`TISUnion/QuickBackupM`](https://github.com/TISUnion/QuickBackupM)。

## 🚪 前置

- MCDReforged >= 2.2.0

## 💻 指令

`!!sync`: 立即同步

`!!sync abort`: 取消同步

## 📄 配置文件

第一次运行时，插件会生成配置文件 **config/foo_bar/config.json**。该文件内容如下：

```json5
{
    "command": "!!sync", // 命令前缀
    "permission": 0, // 权限
    "source_path": "/foo/bar/qb_multi/slot1", // 同步来源，建议设置为主服 QBM 槽位 1
    "world_list": [
        "world" // 存档文件夹名称
    ],
    "server_path": "./server", // 需要同步的世界文件夹列表，原版服务端只会有一个世界
    "backup": false, // 同步前是否进行一次备份以避免小天才
    "backup_path": "./sync_backup", // 备份路径
    "timed_sync": -1, // 定时同步，单位为分钟，<=0 为禁用
    "ignored_files": [
        "seesion.lock" // 同步时忽略的文件。可以 * 作为通配符匹配以某些字符开头或结尾的文件
    ]
}
```
> ⚠️ 此处使用 json5 格式高亮以对配置项进行解释，实际配置格式为 json, 不可使用注释。
