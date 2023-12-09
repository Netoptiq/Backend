import React, { useEffect } from 'react';

const MyComponent = () => {
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = {
          key: 'F3A012DBDB764E07E4AD8B0D3C57A167',
          domain: 'github.com',
          format: 'json',
        };

        let urlStr = 'https://api.ip2whois.com/v2?';

        Object.keys(data).forEach(function (key) {
          if (data[key] !== '') {
            urlStr += key + '=' + encodeURIComponent(data[key]) + '&';
          }
        });

        urlStr = urlStr.substring(0, urlStr.length - 1);

        const response = await fetch(urlStr);
        const result = await response.json();
        
        console.log(result);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {/* Your React component JSX goes here */}
    </div>
  );
};

export default MyComponent;
