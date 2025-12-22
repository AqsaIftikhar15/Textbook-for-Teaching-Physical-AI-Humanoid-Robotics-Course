import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '../../components/ChatWidget';

export default function LayoutWrapper(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatWidget apiEndpoint="#" />
    </>
  );
}
