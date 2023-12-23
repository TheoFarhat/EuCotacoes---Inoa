document.addEventListener('DOMContentLoaded', function () {
    setupWebSocket();
});

function setupWebSocket() {
    const userElement = document.getElementById('user-data');
    const userId = userElement ? userElement.dataset.userId : null;

    console.log('User ID:', userId);

    if (userId) {
        const socket = new WebSocket(`ws://localhost:8000/ws/asset/${userId}/`);

        socket.onopen = function (event) {
            console.log('Conexão websocket funcionando:', event);
        };

        socket.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                console.log('mensagem:', data);

                if (data.type === 'update_asset') {
                    const assetId = data.id;
                    const assetPrice = data.price;
                    const assetPercentageChange = data.percentage_change;
                    updateAssetPrice(assetId, assetPrice, assetPercentageChange);
                } else {
                    console.log('Erro na mensagem:', data.type);
                }
            } catch (error) {
                console.error('Erro recebendo mensagem:', error);
            }
        };

        socket.onclose = function (event) {
            console.log('Conexão websocket fechada:', event);
        };

        function updateAssetPrice(id, price, percentage_change) {
            console.log(`Atualizando asset ${id} com preço ${price}`);
            const assetElementId = `asset-${id}`;
            const assetElement = document.getElementById(assetElementId);      
            if (assetElement) {
                assetElement.querySelector('#price-' + id).innerText = price;
                assetElement.querySelector('#percentage_change-' + id).innerText = percentage_change;
            } else {
                console.log(`Asset element not found for ID ${assetElementId}`);
            }
        }
    } else {
        console.error('User ID não encontrado.');
    }
}
