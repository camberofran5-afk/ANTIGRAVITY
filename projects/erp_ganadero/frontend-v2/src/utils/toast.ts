/**
 * Toast Notification Utilities
 * 
 * Wrapper around react-hot-toast for consistent notifications
 */

import toast from 'react-hot-toast';

/**
 * Show success toast
 */
export const showSuccess = (message: string) => {
    toast.success(message, {
        duration: 3000,
        position: 'top-right',
        style: {
            background: '#10b981',
            color: '#fff',
            fontWeight: '500',
        },
        iconTheme: {
            primary: '#fff',
            secondary: '#10b981',
        },
    });
};

/**
 * Show error toast
 */
export const showError = (message: string) => {
    toast.error(message, {
        duration: 4000,
        position: 'top-right',
        style: {
            background: '#ef4444',
            color: '#fff',
            fontWeight: '500',
        },
        iconTheme: {
            primary: '#fff',
            secondary: '#ef4444',
        },
    });
};

/**
 * Show info toast
 */
export const showInfo = (message: string) => {
    toast(message, {
        duration: 3000,
        position: 'top-right',
        icon: 'ℹ️',
        style: {
            background: '#3b82f6',
            color: '#fff',
            fontWeight: '500',
        },
    });
};

/**
 * Show loading toast
 */
export const showLoading = (message: string) => {
    return toast.loading(message, {
        position: 'top-right',
        style: {
            background: '#6b7280',
            color: '#fff',
            fontWeight: '500',
        },
    });
};

/**
 * Dismiss a specific toast
 */
export const dismissToast = (toastId: string) => {
    toast.dismiss(toastId);
};

/**
 * Dismiss all toasts
 */
export const dismissAllToasts = () => {
    toast.dismiss();
};

/**
 * Promise toast - shows loading, then success or error
 */
export const showPromise = <T,>(
    promise: Promise<T>,
    messages: {
        loading: string;
        success: string;
        error: string;
    }
): Promise<T> => {
    return toast.promise(
        promise,
        {
            loading: messages.loading,
            success: messages.success,
            error: messages.error,
        },
        {
            position: 'top-right',
            style: {
                fontWeight: '500',
            },
        }
    );
};
