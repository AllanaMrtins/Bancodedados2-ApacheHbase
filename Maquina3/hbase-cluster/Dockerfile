FROM eclipse-temurin:17-jdk-jammy

ARG HADOOP_VERSION=3.4.2
ARG HBASE_VERSION=3.0.0
ARG ZK_VERSION=3.9.6

ENV JAVA_HOME=/opt/java/openjdk
ENV HADOOP_HOME=/opt/hadoop
ENV HBASE_HOME=/opt/hbase
ENV ZK_HOME=/opt/zookeeper
ENV PATH=/opt/hadoop/bin:/opt/hadoop/sbin:/opt/hbase/bin:/opt/zookeeper/bin:$PATH

RUN apt-get update && apt-get install -y \
    curl tar bash procps netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fL \
    "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
    -o /tmp/hadoop.tar.gz \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt \
    && mv "/opt/hadoop-${HADOOP_VERSION}" /opt/hadoop \
    && rm /tmp/hadoop.tar.gz

RUN curl -fL \
    "https://archive.apache.org/dist/hbase/${HBASE_VERSION}/hbase-byo-hadoop-${HBASE_VERSION}-bin.tar.gz" \
    -o /tmp/hbase.tar.gz \
    && tar -xzf /tmp/hbase.tar.gz -C /opt \
    && HBASE_DIR="$(find /opt -maxdepth 1 -type d -name 'hbase*' ! -path '/opt/hbase' | head -n 1)" \
    && test -n "$HBASE_DIR" \
    && mv "$HBASE_DIR" /opt/hbase \
    && rm /tmp/hbase.tar.gz

RUN curl -fL \
    "https://archive.apache.org/dist/zookeeper/zookeeper-${ZK_VERSION}/apache-zookeeper-${ZK_VERSION}-bin.tar.gz" \
    -o /tmp/zookeeper.tar.gz \
    && tar -xzf /tmp/zookeeper.tar.gz -C /opt \
    && mv "/opt/apache-zookeeper-${ZK_VERSION}-bin" /opt/zookeeper \
    && rm /tmp/zookeeper.tar.gz

RUN groupadd -r hadoop \
    && useradd -r -g hadoop -m -d /home/hadoop hadoop \
    && mkdir -p \
       /data/hadoop/nn \
       /data/hadoop/dn \
       /data/hadoop/tmp \
       /data/zookeeper \
       /data/hbase \
    && chown -R hadoop:hadoop \
       /opt/hadoop /opt/hbase /opt/zookeeper /data /home/hadoop

RUN printf '\nexport JAVA_HOME=/opt/java/openjdk\n' \
    >> /opt/hadoop/etc/hadoop/hadoop-env.sh \
    && printf '\nexport JAVA_HOME=/opt/java/openjdk\nexport HADOOP_HOME=/opt/hadoop\n' \
    >> /opt/hbase/conf/hbase-env.sh

USER hadoop
WORKDIR /home/hadoop

CMD ["bash"]
