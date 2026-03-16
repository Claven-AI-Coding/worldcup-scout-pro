import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EmptyState from '@/components/common/EmptyState.vue'

describe('EmptyState', () => {
  it('renders with default props', () => {
    const wrapper = mount(EmptyState, { props: { message: 'No data' } })
    expect(wrapper.exists()).toBe(true)
  })

  it('displays custom message', () => {
    const message = 'No data available'
    const wrapper = mount(EmptyState, { props: { message } })
    expect(wrapper.text()).toContain(message)
  })

  it('displays custom description', () => {
    const message = 'Try again later'
    const wrapper = mount(EmptyState, { props: { message } })
    expect(wrapper.text()).toContain(message)
  })

  it('renders no-data icon', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-data', message: 'No data' } })
    const svg = wrapper.find('svg')
    expect(svg.exists()).toBe(true)
  })

  it('renders no-network icon', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-network', message: 'No network' } })
    const svg = wrapper.find('svg')
    expect(svg.exists()).toBe(true)
  })

  it('renders no-permission icon', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-permission', message: 'No permission' } })
    const svg = wrapper.find('svg')
    expect(svg.exists()).toBe(true)
  })

  it('shows action button when actionText provided', async () => {
    const wrapper = mount(EmptyState, {
      props: { message: 'No data', actionText: 'Retry' },
    })
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
    await button.trigger('click')
    expect(wrapper.emitted('action')).toBeTruthy()
  })

  it('shows default action for no-network type', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-network', message: 'No network' } })
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
    expect(button.text()).toBe('重新加载')
  })

  it('shows default action for no-permission type', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-permission', message: 'No permission' } })
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
    expect(button.text()).toBe('去登录')
  })

  it('hides button when no action', () => {
    const wrapper = mount(EmptyState, { props: { type: 'no-data', message: 'No data' } })
    const button = wrapper.find('button')
    expect(button.exists()).toBe(false)
  })
})
