import AsyncComponentLoading from './AsyncComponentLoading';
import AsyncComponentError from './AsyncComponentError';

export default (
  promise,
  delay = undefined, // delay before display to avoid flickering
  timeout = undefined,
) => () => ({
  component: promise,
  loading: AsyncComponentLoading,
  error: AsyncComponentError,
  delay: ((delay === undefined) ? 200 : delay),
  timeout,
});
