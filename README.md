## Chesterbot Downloads Discord Images

I created this to download the images in specific Discord channels.

You'll need to configure a config.json that looks like this:

```
{
    "token" : "YOUR DISCORD BOT's API TOKEN",
    "image_dir_root" : "./images",
    "delay_secs" : 5,
    "loop_delay_secs" : 0.1,
    "channel_id" : 1188501030695092225,
    "message_quantity" : 10000
}
```

And then just run it.

I've found that your Bot will need Administrator privileges otherwise an exception is thrown when reading channel.history, which is weird because there is a Channel History permission scoping. Without the Administrator privileges, the bot crashes. Sad.

Also, I'm not entirely sure that this Bot will gather all messages. You can't get a message quantity from the channel nor an enumeration of all the messages in the channel. Sad.

So it's a bit of a brute force thing. Set message quantity ridiculously high, and run it.