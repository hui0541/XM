import com.alibaba.fastjson.JSON;
import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.DatagramPacket;
import io.netty.channel.socket.nio.NioDatagramChannel;
import io.netty.util.CharsetUtil;

/**
 * 对应文件：交易网关服务.java (新增入口)
 * 职责：启动交易网关，监听策略指令
 * 运行方式：java 交易网关服务
 */
public class 交易网关服务 {

    private static final int LISTEN_PORT = 8888;

    // 组件实例
    private static 券商交易接口 brokerInterface;
    private static 订单撮合与回报 oms;

    public static void main(String[] args) {
        System.out.println(">>> A股极速交易网关 (Java Core) 启动...");

        // 1. 初始化 OMS
        oms = new 订单撮合与回报();

        // 2. 初始化券商接口 (这里使用模拟器，可替换为 CTP 实现)
        brokerInterface = new 交易接口适配器_示例();
        brokerInterface.setCallback(oms);
        brokerInterface.init("sim_account_001");

        // 3. 启动 Netty 监听策略指令 (UDP)
        startCommandListener();
    }

    private static void startCommandListener() {
        EventLoopGroup group = new NioEventLoopGroup(1);
        try {
            Bootstrap b = new Bootstrap();
            b.group(group)
                    .channel(NioDatagramChannel.class)
                    .option(ChannelOption.SO_BROADCAST, true)
                    .handler(new SimpleChannelInboundHandler<DatagramPacket>() {
                        @Override
                        protected void channelRead0(ChannelHandlerContext ctx, DatagramPacket packet) {
                            // 1. 接收策略指令 (JSON)
                            ByteBuf content = packet.content();
                            String jsonStr = content.toString(CharsetUtil.UTF_8);

                            try {
                                // 2. 解析
                                券商交易接口.OrderRequest req = JSON.parseObject(jsonStr, 券商交易接口.OrderRequest.class);
                                if (req != null) {
                                    System.out
                                            .println("[Gateway] 收到策略指令: " + req.getSymbol() + " -> " + req.getAction());

                                    // 3. 执行报单
                                    String orderId = brokerInterface.insertOrder(req);

                                    // 4. 登记到 OMS
                                    oms.registerOrder(orderId, req.getSymbol());
                                }
                            } catch (Exception e) {
                                System.err.println("[Gateway] 指令解析失败: " + e.getMessage());
                            }
                        }
                    });

            System.out.println(">>> 交易指令监听中 @ UDP " + LISTEN_PORT);
            b.bind(LISTEN_PORT).sync().channel().closeFuture().await();

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            group.shutdownGracefully();
        }
    }}```

    ###💡模块交付总结

    **交易执行模块(Java)**已构建完成。

    1.**输入**：

    监听 UDP 8888
    端口的 JSON 指令。2.**处理**：`交易网关服务`解析指令->`券商交易接口`执行报单->`订单撮合与回报`管理状态。3.**输出**：控制台实时打印带颜色的订单状态变更日志。

    **如何测试？**由于`策略引擎模块`
    中的 Python
    代码目前只打印了 Signal
    而未发送 UDP，
    您可以在 Python 策略中添加以下简单的发送逻辑来闭环测试：

    ```python#

简单的测试脚本 (Python)
    import socket,json sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)order={"symbol":"sh600000","direction":1,"price":10.5,"quantity":100}sock.sendto(json.dumps(order).encode('utf-8'),("127.0.0.1",8888))sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)order={"symbol":"sh600000","direction":1,"price":10.5,"quantity":100}sock.sendto(json.dumps(order).encode('utf-8'),("127.0.0.1",8888)
)