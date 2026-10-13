seshat-workload-platform on  main [?] via 💠 default on ☁️  (us-east-1) 
Beach_Life cat apps/ueransim/gnb-configmap.yaml apps/ueransim/ue-configmap.yaml apps/upf/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ueransim-gnb-config
  namespace: default
data:
  open5gs-gnb.yaml.template: |
    mcc: '999'
    mnc: '70'

    nci: '0x000000010'
    idLength: 32
    tac: 1

    linkIp: ${POD_IP}
    ngapIp: ${POD_IP}
    gtpIp: ${N3_IP}

    amfConfigs:
      - address: ${AMF_IP}
        port: 38412

    slices:
      - sst: 1
        sd: 1118481

    ignoreStreamIds: true
apiVersion: v1
kind: ConfigMap
metadata:
  name: ueransim-ue-config
  namespace: default

data:
  open5gs-ue.yaml.template: |
    supi: 'imsi-999700000000001'
    mcc: '999'
    mnc: '70'

    protectionScheme: 0
    homeNetworkPublicKey: '0000000000000000000000000000000000000000000000000000000000000000'
    homeNetworkPublicKeyId: 1
    routingIndicator: '0000'

    key: '465B5CE8B199B49FAA5F0A2EE238A6BC'
    op: 'E8ED289DEBA952E4283B54E88E6183CA'
    opType: 'OPC'
    amf: '8000'

    imei: '356938035643803'
    imeiSv: '4370816125816151'

    gnbSearchList:
      - ${GNB_IP}

    uacAic:
      mps: false
      mcs: false

    uacAcc:
      normalClass: 0
      class11: false
      class12: false
      class13: false
      class14: false
      class15: false

    sessions:
      - type: 'IPv4'
        apn: 'internet'
        slice:
          sst: 1
          sd: 1118481

    configured-nssai:
      - sst: 1
        sd: 1118481

    default-nssai:
      - sst: 1
        sd: 1118481

    integrity:
      IA1: true
      IA2: true
      IA3: true

    ciphering:
      EA1: true
      EA2: true
      EA3: true

    integrityMaxRate:
      uplink: 'full'
      downlink: 'full'apiVersion: v1
kind: ConfigMap
metadata:
  name: telco-data-plane-config  # Flux is getting this
  namespace: default
  labels:
    app: upf-core
    managed-by: flux
data:
  upf.yaml: |
    logger:
      path:
        file: /opt/open5gs/var/log/open5gs/upf.log
    global:
      max:
        ue: 1024

    # N4 Interface
    # UPF listens for PFCP session rules from the SMF on UDP 8805
    upf:
      pfcp:
        server:
        - dev: eth0

    # N3 INTERFACE
    # gtp-u traffic - Port 2152
      gtpu:
        server:
          - dev: n3


    # N6 Forwarding is taken care of by Linux
      session:
        - subnet: 10.45.0.0/16
          gateway: 10.45.0.1
          dnn: internet

      metrics:
        server:
          - dev: eth0
            port: 9090

seshat-workload-platform on  main [?] via 💠 default on ☁️
