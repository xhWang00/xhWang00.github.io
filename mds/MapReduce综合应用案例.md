---
title: MapReduce综合应用案例
date: 2026-05-26
---

# MapReduce综合应用案例

大数据技术2026学年第一学期，实验6参考笔记

## 6.1 MapReduce综合应用案例 — 电信数据清洗

### LongMR.java

```java
package com;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**MapReduce操作类*/
public class LogMR {
    // 定义 HDFS 输入源和输出目的地路径
    private static final String INPUT_PATH = "/user/test/input/a.txt";
    private static final String OUTPUT_PATH = "/user/test/output";

    /**
     * Mapper 类：负责读取 HDFS 文本并结合 MySQL 缓存进行数据清洗
     */
    public static class CleanMapper extends Mapper<LongWritable, Text, Text, NullWritable> {
        // 内存缓存：用于存放从 MySQL 中预加载的数据
        private Map<String, String> userMap = new HashMap<>();
        private Map<String, String> regionMap = new HashMap<>();
        // 时间格式化工具
        private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        /**
         * setup 方法在 map 任务启动时最先执行一次
         * 在这里连接 MySQL 数据库，将数据加载到 Map 集合中
         */
        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            Connection conn = null;
            Statement stmt = null;
            ResultSet rsUser = null;
            ResultSet rsRegion = null;
            try {
                // 注册并加载 MySQL 驱动
                Class.forName("com.mysql.jdbc.Driver");
                // 建立连接
                conn = java.sql.DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=utf8", 
                    "root", 
                    "123123"
                );
                stmt = conn.createStatement();

                // 1. 预加载用户手机号与真实姓名的映射
                rsUser = stmt.executeQuery("select phone, trueName from userphone");
                while (rsUser.next()) {
                    String phone = rsUser.getString("phone");
                    String trueName = rsUser.getString("trueName");
                    if (phone != null && trueName != null) {
                        userMap.put(phone, trueName);
                    }
                }

                // 2. 预加载省份编码与省份名称的映射
                rsRegion = stmt.executeQuery("select CodeNum, Address from allregion");
                while (rsRegion.next()) {
                    String codeNum = rsRegion.getString("CodeNum");
                    String address = rsRegion.getString("Address");
                    if (codeNum != null && address != null) {
                        regionMap.put(codeNum, address);
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                // 关闭数据库连接资源，释放内存
                try { if (rsUser != null) rsUser.close(); } catch (SQLException e) {}
                try { if (rsRegion != null) rsRegion.close(); } catch (SQLException e) {}
                try { if (stmt != null) stmt.close(); } catch (SQLException e) {}
                try { if (conn != null) conn.close(); } catch (SQLException e) {}
            }
        }

        /**
         * map 方法对文件的每一行进行清洗转换
         */
        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            // 将一行文本转换为字符串并去除首尾空格
            String line = value.toString().trim();
            if (line.isEmpty()) return;

            // 切分数据
            String[] fields = line.split(",");
            if (fields.length < 6) return;

            // 提取原始字段数据
            String callerPhone = fields[0];
            String receiverPhone = fields[1];
            long startTimeSec = Long.parseLong(fields[2]);
            long endTimeSec = Long.parseLong(fields[3]);
            String callerRegionCode = fields[4];
            String receiverRegionCode = fields[5];

            // 1. 关联真实姓名 (若在缓存中未找到则保留原样或标记未知)
            String callerName = userMap.getOrDefault(callerPhone, "未知");
            String receiverName = userMap.getOrDefault(receiverPhone, "未知");

            // 2. 转换时间戳格式 (秒级时间戳需要乘以 1000L 转换为毫秒)
            String startTimeStr = sdf.format(startTimeSec * 1000L);
            String endTimeStr = sdf.format(endTimeSec * 1000L);

            // 3. 计算通话时长 (秒)
            long duration = endTimeSec - startTimeSec;

            // 4. 关联省份名称
            String callerAddress = regionMap.getOrDefault(callerRegionCode, "未知省份");
            String receiverAddress = regionMap.getOrDefault(receiverRegionCode, "未知省份");

            // 5. 按照目标格式拼接字符串数据
            StringBuilder sb = new StringBuilder();
            sb.append(callerName).append(",")
              .append(receiverName).append(",")
              .append(callerPhone).append(",")
              .append(receiverPhone).append(",")
              .append(startTimeStr).append(",")
              .append(endTimeStr).append(",")
              .append(duration).append(",")
              .append(callerAddress).append(",")
              .append(receiverAddress);

            // 输出清洗后的整行文本
            context.write(new Text(sb.toString()), NullWritable.get());
        }
    }

    /**
     * Driver 驱动方法：配置并提交 MapReduce 任务
     */
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Log Clean Job");

        job.setJarByClass(LogMR.class);
        job.setMapperClass(CleanMapper.class);

        // 数据清洗场景不需要 Reduce 聚合阶段，直接设置 Reduce 任务数为 0 提高效率
        job.setNumReduceTasks(0);

        // 设置输出数据的 Key 和 Value 的 Class 类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);

        Path inputPath = new Path(INPUT_PATH);
        Path outputPath = new Path(OUTPUT_PATH);

        // 检查 HDFS 上输出路径是否存在，若存在则提前删除，防止报错
        FileSystem fs = FileSystem.get(conf);
        if (fs.exists(outputPath)) {
            fs.delete(outputPath, true);
        }

        // 设置输入输出的 HDFS 文件路径
        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outputPath);

        // 提交作业并等待执行结束
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

**代码说明：**  
`LogMR` 是一个只有 Mapper 阶段的 MapReduce 程序，负责将 HDFS 的原始通话记录与 MySQL 中的用户/地区信息进行关联清洗。  

1. **`CleanMapper.setup()`** — Map 任务启动时执行一次：通过 JDBC 连接 MySQL，将 `userphone` 表（手机号 → 真实姓名）和 `allregion` 表（编码 → 省份名称）全部加载到内存的 `HashMap` 中，然后关闭连接。  
2. **`CleanMapper.map()`** — 对输入文件的每一行依次执行：  
   - 按逗号切分，提取主叫/被叫手机号、开始/结束时间戳、地区编码；  
   - 从 `userMap` 缓存查询真实姓名（未找到则标记为"未知"）；  
   - 将秒级时间戳转为毫秒，格式化为 `yyyy-MM-dd HH:mm:ss`；  
   - 计算通话时长（结束时间 − 开始时间）；  
   - 从 `regionMap` 缓存查询省份名称；  
   - 拼接为逗号分隔的清洗后文本并输出。  
3. **`main()`** — 配置 Job：设置 Mapper 为 `CleanMapper`，Reduce 任务数为 0（纯清洗无需聚合），自动清理输出目录，提交任务等待完成。  


---

## 6.2 MapReduce综合应用案例 — 招聘数据清洗

### DBHelper.java

```java
package com;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBHelper {
    /********** begin **********/
    private static final String driver = "com.mysql.jdbc.Driver";
    private static final String url = "jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8";
    private static final String username = "root";
    private static final String password = "123123";
    private static Connection conn = null;
    static {
        try {
            Class.forName(driver);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    public static Connection getConnection() {
        if (conn == null) {
            try {
                conn = DriverManager.getConnection(url, username, password);
            } catch (SQLException e) {
                e.printStackTrace();
            }
            return conn;
        }
        return conn;
    }
    public static void main(String[] args) {
        Connection connection = DBHelper.getConnection();
    }
    /********** end **********/
}
```

**代码说明：**  
`DBHelper` 是一个 MySQL 数据库连接工具类，采用单例模式管理连接对象。  

1. **静态代码块** — 类加载时通过 `Class.forName()` 注册 MySQL JDBC 驱动。  
2. **`getConnection()`** — 如果 `conn` 为 null 则创建新连接，否则直接返回已有连接，避免重复创建数据库连接，提高资源利用率。  


### JsonMap.java

```java
package com;
import com.alibaba.fastjson.JSONObject;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;

public class JsonMap  extends Mapper<LongWritable, Text, NullWritable, Put> {

    /********** begin **********/
    Map<String, String> pro = new HashMap<String, String>();
    Put put;
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        Connection connection = DBHelper.getConnection();
        try {
            Statement statement = connection.createStatement();
            String sql = "select * from province";
            ResultSet resultSetA = statement.executeQuery(sql);
            while (resultSetA.next()) {
                String city_code = resultSetA.getString(1);
                String city_name = resultSetA.getString(2);
                pro.put(city_code, city_name);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    public void map(LongWritable key,Text value,Context context) throws IOException, InterruptedException {
        String line = value.toString();
        //解析json数据
        JSONObject jsonObject = JSONObject.parseObject(line);
        String[] data = new String[14];
        data[0] = jsonObject.getString("id");
        data[1] = jsonObject.getString("company_name");
        data[2] = jsonObject.getString("eduLevel_name");
        data[3] = jsonObject.getString("emplType");
        data[4] = jsonObject.getString("jobName");
        String salary=jsonObject.getString("salary");
        if (salary.contains("K-")) {
             Double a =Double.valueOf(salary.substring(0,salary.indexOf("K")));
             Double b =Double.valueOf(salary.substring(salary.indexOf("-")+1,salary.lastIndexOf("K")));
            data[5] = (a+b)/2+"";
        }else {
            data[5]="0";
        }
        data[6] = jsonObject.getString("createDate");
        data[7] = jsonObject.getString("endDate");
        String code = jsonObject.getString("city_code");
        //data[8] = pro.get(code);
        data[8] = code;
        data[9] = jsonObject.getString("companySize");
        data[10] = jsonObject.getString("welfare");
        data[11] = jsonObject.getString("responsibility");
        data[12] = jsonObject.getString("place");
        data[13] = jsonObject.getString("workingExp");
        //循环判空
        for(String i : data) {
            if(i==null||i.equals("")) {
                return;
            }
        }
        String columnFamily = "info";
        put= new Put(data[0].getBytes());
        put.addColumn(columnFamily.getBytes(), "company_name".getBytes(), data[1].getBytes());
        put.addColumn(columnFamily.getBytes(), "eduLevel_name".getBytes(), data[2].getBytes());
        put.addColumn(columnFamily.getBytes(), "emplType".getBytes(), data[3].getBytes());
        put.addColumn(columnFamily.getBytes(), "jobName".getBytes(), data[4].getBytes());
        put.addColumn(columnFamily.getBytes(), "salary".getBytes(), data[5].getBytes());
        put.addColumn(columnFamily.getBytes(), "createDate".getBytes(), data[6].getBytes());
        put.addColumn(columnFamily.getBytes(), "endDate".getBytes(), data[7].getBytes());
        put.addColumn(columnFamily.getBytes(), "city_name".getBytes(), data[8].getBytes());
        put.addColumn(columnFamily.getBytes(), "companySize".getBytes(), data[9].getBytes());
        put.addColumn(columnFamily.getBytes(), "welfare".getBytes(), data[10].getBytes());
        put.addColumn(columnFamily.getBytes(), "responsibility".getBytes(), data[11].getBytes());
        put.addColumn(columnFamily.getBytes(), "place".getBytes(), data[12].getBytes());
        put.addColumn(columnFamily.getBytes(), "workingExp".getBytes(), data[13].getBytes());
        context.write(NullWritable.get(), put);
    }
    /********** end **********/
}
```

**代码说明：**  
`JsonMap` 是一个 MapReduce Mapper，负责解析 JSON 格式的招聘数据并写入 HBase 表。  

1. **`setup()`** — 任务启动时通过 `DBHelper.getConnection()` 连接 MySQL，将 `province` 表（城市编码 → 城市名称）加载到内存缓存 `pro` 中。  
2. **`map()`** — 对每行 JSON 依次执行：  
   - 用 FastJSON 解析文本行为 `JSONObject`；  
   - 提取 id、公司名称、学历要求等 14 个字段；  
   - 薪资特殊处理：若包含 `"K-"` 则取上下限的平均值，否则置为 `"0"`；  
   - 遍历数组判空，任一字段为空则跳过该行；  
   - 构造 HBase 的 `Put` 对象，以 id 为行键，`info` 列族下写入所有字段；  
   - 通过 `context.write()` 将 Put 输出到 HBase。  


### JsonTest.java

```java
package com;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptor;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptorBuilder;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.TableDescriptorBuilder;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;

public class JsonTest {
    public static void main(String[] args) throws Exception{
        
        Configuration config = HBaseConfiguration.create();
        //设置zookeeper的配置
        config.set("hbase.zookeeper.quorum", "127.0.0.1");
        Connection connection = ConnectionFactory.createConnection(config);
        Admin admin = connection.getAdmin();
        TableName tableName = TableName.valueOf("job");
        boolean isExists = admin.tableExists(tableName);
        if (!isExists) {
            TableDescriptorBuilder tableDescriptor = TableDescriptorBuilder.newBuilder(tableName);
            ColumnFamilyDescriptor family = ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("info")).build();// 构建列族对象
            tableDescriptor.setColumnFamily(family); // 设置列族
            admin.createTable(tableDescriptor.build()); // 创建表
        } else {
            admin.disableTable(tableName);
            admin.deleteTable(tableName);
            TableDescriptorBuilder tableDescriptor = TableDescriptorBuilder.newBuilder(tableName);
            ColumnFamilyDescriptor family = ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("info")).build();// 构建列族对象
            tableDescriptor.setColumnFamily(family); // 设置列族
            admin.createTable(tableDescriptor.build()); // 创建表
        }

        /********** begin **********/
        Job job = Job.getInstance(config);
        job.setJarByClass(JsonTest.class);
        job.setMapperClass(JsonMap.class);
        job.setMapOutputKeyClass(NullWritable.class);
        //只有map没有reduce，所以设置reduce的数目为0
        job.setNumReduceTasks(0);
        //设置数据的输入路径,没有使用参数，直接在程序中写入HDFS的路径
        FileInputFormat.setInputPaths(job, new Path("/root/data/data.json"));
        //驱动函数
        TableMapReduceUtil.initTableReducerJob("job",null, job);
        TableMapReduceUtil.addDependencyJars(job);
        job.waitForCompletion(true);
        /********** end **********/
    }
}
```

**代码说明：**  
`JsonTest` 是 MapReduce 驱动类，负责创建 HBase 表并提交数据导入任务。  

1. **HBase 表管理** — 通过 `HBaseConfiguration` 连接 ZooKeeper，检查 `job` 表是否存在：不存在则创建，存在则删除重建，均包含 `info` 列族。  
2. **MapReduce Job 配置** — 设置 Mapper 为 `JsonMap`，Reducer 数为 0（不需要聚合）；输入路径为 HDFS 的 `/root/data/data.json`；通过 `TableMapReduceUtil.initTableReducerJob("job", null, job)` 将输出写入 HBase 的 `job` 表；提交任务等待完成。  

