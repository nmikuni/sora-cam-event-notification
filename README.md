# Motion detection and notification App with Soracom Cloud Camera Service

Soracom Cloud Camera Service (ソラカメ) のモーション検知イベントを SORACOM API で取得し、画像を LINE Notify で通知するアプリケーションです。AWS Serverless Application Model (SAM) テンプレートを用いてデプロイできます。

**デフォルトで 1 分ごとに実行されるので注意してください。**

## 構成

1. Amazon EventBridge で定期的に AWS Lambda を呼び出す
2. ソラカメ API で過去 1 分のイベント一覧を取得
3. イベント発生時の静止画像をダウンロード
4. ダウンロードした画像を LINE Notify で通知

(イベントが複数あった場合、3, 4 は全てのイベントに対して実施)

## 利用手順

以下の手順で利用できます。

### 事前準備

アカウントや環境を準備してください。

1. [Soracom Cloud Camera Service](https://soracom.jp/sora_cam/) 対応のカメラを用意する (API の利用にはライセンスの契約も必要です)
2. [LINE Notify](https://notify-bot.line.me/ja/) をセットアップする
3. [AWS](https://aws.amazon.com/jp/?nc2=h_lg) アカウントを用意する
4. [SORACOM SAM ユーザー](https://users.soracom.io/ja-jp/docs/sam/) の認証情報 (認証キー ID、認証キー) を準備する
5. [AWS Serverless Application Model](https://aws.amazon.com/jp/serverless/sam/) (SAM) をセットアップする
   - この手順においては、SAM の利用にあたって Docker の準備も合わせて必要です。

### アプリケーションのデプロイ

3. `sora-cam-event-notification` のデプロイのため、必要な環境変数を準備します。
   - soracomAuthKeyId: SORACOM SAM ユーザーの認証キー ID
   - soracomAuthKey: SORACOM SAM ユーザーの認証キー
   - deviceId: ソラカメ対応カメラのデバイス ID
   - lineNotifyToken: LINE Notify のトークン
4. `sora-cam-event-notification` をビルド・デプロイします
   - `sam build` `sam deploy --guided` を用います

### アプリケーションの削除

SAM でデプロイしたアプリケーションは CloudFormation から削除できます。