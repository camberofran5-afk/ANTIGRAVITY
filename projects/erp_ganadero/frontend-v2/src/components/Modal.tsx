import React, { useEffect } from 'react';

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === 'Escape' && isOpen) {
                onClose();
            }
        };

        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    const backdropStyles: React.CSSProperties = {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        animation: 'fadeIn 0.2s ease'
    };

    const modalStyles: React.CSSProperties = {
        backgroundColor: 'white',
        borderRadius: 'var(--radius-lg)',
        padding: '2rem',
        maxWidth: '600px',
        width: '90%',
        maxHeight: '90vh',
        overflowY: 'auto',
        boxShadow: 'var(--shadow-lg)',
        animation: 'slideUp 0.3s ease'
    };

    const headerStyles: React.CSSProperties = {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem',
        paddingBottom: '1rem',
        borderBottom: '2px solid var(--border)'
    };

    const titleStyles: React.CSSProperties = {
        fontSize: '1.5rem',
        fontWeight: 600,
        color: 'var(--text-primary)',
        margin: 0
    };

    const closeButtonStyles: React.CSSProperties = {
        background: 'none',
        border: 'none',
        fontSize: '2rem',
        cursor: 'pointer',
        color: 'var(--text-secondary)',
        padding: '0.25rem 0.5rem',
        lineHeight: 1,
        transition: 'var(--transition-normal)'
    };

    return (
        <div style={backdropStyles} onClick={onClose}>
            <div style={modalStyles} onClick={(e) => e.stopPropagation()}>
                <div style={headerStyles}>
                    <h2 style={titleStyles}>{title}</h2>
                    <button
                        style={closeButtonStyles}
                        onClick={onClose}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.color = 'var(--text-primary)';
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.color = 'var(--text-secondary)';
                        }}
                    >
                        ×
                    </button>
                </div>
                {children}
            </div>
            <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
        </div>
    );
};

export default Modal;
