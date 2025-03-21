from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # 获取环境变量中的端口，如果没有则使用默认值 5000
    port = int(os.environ.get('SERVER_PORT', 5000))
    app.run(host='0.0.0.0', port=port)