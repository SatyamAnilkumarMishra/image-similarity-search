import React from 'react';

function StatusMessage({ status }) {
  if (!status.message) return null;

  return (
    <div className={`status ${status.type}`}>
      {status.message}
    </div>
  );
}

export default StatusMessage;
