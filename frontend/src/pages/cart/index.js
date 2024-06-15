import { PurchaseList, Title, Container, Main, Button } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect, useState } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const Cart = ({ updateOrders, orders }) => {
  const {
    recipes,
    setRecipes,
    handleAddToCart
  } = useRecipes()
  
  const getRecipes = () => {
    api
      .getRecipes({
        page: 1,
        limit: 999,
        is_in_shopping_cart: Number(true)
      })
      .then(res => {
        const { results } = res
        setRecipes(results)
      })
  }

  useEffect(_ => {
    getRecipes()
  }, [])

  const downloadDocument = (format) => {
    const filename = format === 'json' ? 'shopping_cart.json' : 'shopping_cart.txt';
    api.downloadFile(format)
      .then(response => {
        if (response.ok) {
          return response.blob();
        } else {
          throw new Error('Ошибка при загрузке файла');
        }
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        downloadFileFromUrl(url, filename);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }

  const downloadFileFromUrl = (url, filename) => {
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
  }

  const downloadTxtDocument = () => {
    api.downloadTxtFile()
      .then(response => {
        if (response.ok) {
          return response.blob().then(blob => {
            const url = window.URL.createObjectURL(blob);
            downloadFileFromUrl(url, 'shopping_cart.txt');
          });
        } else {
          throw new Error('Ошибка при загрузке файла');
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }

  const downloadPDFDocument = () => {
    api.downloadPDFFile()
      .then(response => {
        if (response.ok) {
          return response.blob().then(blob => {
            const url = window.URL.createObjectURL(blob);
            downloadFileFromUrl(url, 'shopping_cart.pdf');
          });
        } else {
          throw new Error('Ошибка при загрузке файла');
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }
  return <Main>
    <Container className={styles.container}>
      <MetaTags>
        <title>Список покупок</title>
        <meta name="description" content="Фудграм - Список покупок" />
        <meta property="og:title" content="Список покупок" />
      </MetaTags>
      <div className={styles.cart}>
        <Title title='Список покупок' />
        <PurchaseList
          orders={recipes}
          handleRemoveFromCart={handleAddToCart}
          updateOrders={updateOrders}
        />
        {orders > 0 && (
          <div>
            <p>Скачать список покупок:</p>
            <Button
              modifier='style_dark'
              clickHandler={downloadTxtDocument}
              style={{ marginRight: '10px' }}
            >
              txt
            </Button>
            <Button
              modifier='style_dark'
              clickHandler={downloadPDFDocument}
            >
              pdf
            </Button>
          </div>
        )}
      </div>
    </Container>
  </Main>
}

export default Cart

